# -*- coding: utf-8 -*-
"""
Pre-built example workflow templates for the Visual AI Automation Workflow Builder
"""

import uuid
from langgraph.graph import END
from src.config.constants import END_NODE_ID

def get_simple_summarizer_workflow():
    """
    Returns a simple single-node workflow that summarizes input text
    """
    node_id = f"summarize_node_{uuid.uuid4().hex[:4]}"
    return [
        {
            "id": node_id,
            "name": "Summarize Input",
            "prompt": "Summarize the input text concisely (1-2 sentences).",
            "type": "llm_call",
            "routing_rules": {
                "default_target": END_NODE_ID,
                "conditional_targets": [
                    {"output_key": "done", "target_node_id": END_NODE_ID}
                ]
            }
        }
    ]

def get_sentiment_workflow():
    """
    Returns a sentiment analysis workflow with branching paths based on detected sentiment
    """
    ids = {name: f"sentiment_node_{uuid.uuid4().hex[:4]}" for name in [
        "analyzer", "positive", "negative", "neutral"
    ]}
    
    nodes = [
        {
            "id": ids["analyzer"],
            "name": "Analyze Sentiment",
            "prompt": "Analyze sentiment (Positive, Negative, Neutral) of the input. Respond ONLY with the result.",
            "type": "llm_call",
            "routing_rules": {
                "default_target": ids["neutral"],
                "conditional_targets": [
                    {"output_key": "Positive", "target_node_id": ids["positive"]},
                    {"output_key": "Negative", "target_node_id": ids["negative"]},
                    {"output_key": "Neutral", "target_node_id": ids["neutral"]}
                ]
            }
        },
        {
            "id": ids["positive"],
            "name": "Handle Positive",
            "prompt": "Sentiment was positive. Respond cheerfully.",
            "type": "llm_call",
            "routing_rules": {
                "default_target": END_NODE_ID,
                "conditional_targets": [
                    {"output_key": "done", "target_node_id": END_NODE_ID}
                ]
            }
        },
        {
            "id": ids["negative"],
            "name": "Handle Negative",
            "prompt": "Sentiment was negative. Respond empathetically.",
            "type": "llm_call",
            "routing_rules": {
                "default_target": END_NODE_ID,
                "conditional_targets": [
                    {"output_key": "done", "target_node_id": END_NODE_ID}
                ]
            }
        },
        {
            "id": ids["neutral"],
            "name": "Handle Neutral",
            "prompt": "Sentiment was neutral. Acknowledge receipt.",
            "type": "llm_call",
            "routing_rules": {
                "default_target": END_NODE_ID,
                "conditional_targets": [
                    {"output_key": "done", "target_node_id": END_NODE_ID}
                ]
            }
        }
    ]
    
    return nodes

def get_classification_workflow():
    """
    Returns a workflow that extracts and classifies user intent, then handles accordingly
    """
    ids = {name: f"classify_node_{uuid.uuid4().hex[:4]}" for name in [
        "classify", "complaint", "query", "compliment", "general"
    ]}
    
    nodes = [
        {
            "id": ids["classify"],
            "name": "Extract & Classify Intent",
            "prompt": "From input, extract product/person (or 'None'). Classify intent: Complaint, Query, Compliment. Respond STRICTLY:\nExtracted Info: [Info]\nIntent: [IntentWord]",
            "type": "llm_call",
            "routing_rules": {
                "default_target": ids["general"],
                "conditional_targets": [
                    {"output_key": "Complaint", "target_node_id": ids["complaint"]},
                    {"output_key": "Query", "target_node_id": ids["query"]},
                    {"output_key": "Compliment", "target_node_id": ids["compliment"]}
                ]
            }
        },
        {
            "id": ids["complaint"],
            "name": "Handle Complaint",
            "prompt": "Complaint received. Respond empathetically, use extracted info.",
            "type": "llm_call",
            "routing_rules": {
                "default_target": END_NODE_ID,
                "conditional_targets": [
                    {"output_key": "done", "target_node_id": END_NODE_ID}
                ]
            }
        },
        {
            "id": ids["query"],
            "name": "Answer Query",
            "prompt": "Query received. Answer based on context/info. Use web search if needed.",
            "type": "llm_call",
            "routing_rules": {
                "default_target": END_NODE_ID,
                "conditional_targets": [
                    {"output_key": "done", "target_node_id": END_NODE_ID}
                ]
            }
        },
        {
            "id": ids["compliment"],
            "name": "Handle Compliment",
            "prompt": "Compliment received. Respond thankfully.",
            "type": "llm_call",
            "routing_rules": {
                "default_target": END_NODE_ID,
                "conditional_targets": [
                    {"output_key": "done", "target_node_id": END_NODE_ID}
                ]
            }
        },
        {
            "id": ids["general"],
            "name": "General Response",
            "prompt": "Intent unclear. Provide generic response.",
            "type": "llm_call",
            "routing_rules": {
                "default_target": END_NODE_ID,
                "conditional_targets": [
                    {"output_key": "done", "target_node_id": END_NODE_ID}
                ]
            }
        }
    ]
    
    return nodes

def get_deep_research_workflow():
    """
    Returns a multi-stage research workflow with various angles and cross-referencing
    """
    ids = {name: f"dr_node_{uuid.uuid4().hex[:4]}" for name in [
        "planner", "search_A", "search_B", "cross_reference", "synthesize", "final_report"
    ]}
    
    nodes = [
        {
            "id": ids["planner"],
            "name": "📝 Research Planner",
            "prompt": "Analyze the research goal. Break into 1-3 angles (A, B). State plan. Decide if single/multi angle needed.",
            "type": "llm_call",
            "routing_rules": {
                "default_target": ids["search_A"],
                "conditional_targets": [
                    {"output_key": "single_angle", "target_node_id": ids["search_A"]},
                    {"output_key": "multi_angle", "target_node_id": ids["search_A"]}
                ]
            }
        },
        {
            "id": ids["search_A"],
            "name": "🔍 Research Angle A",
            "prompt": "Research Angle A based on plan. Use web search if necessary. Summarize findings for Angle A.",
            "type": "llm_call",
            "routing_rules": {
                "default_target": ids["search_B"],
                "conditional_targets": [
                    {"output_key": "synthesize_direct", "target_node_id": ids["synthesize"]},
                    {"output_key": "next_angle", "target_node_id": ids["search_B"]}
                ]
            }
        },
        {
            "id": ids["search_B"],
            "name": "🔎 Research Angle B",
            "prompt": "Research Angle B based on plan. Use web search if necessary. Summarize findings for Angle B.",
            "type": "llm_call",
            "routing_rules": {
                "default_target": ids["cross_reference"],
                "conditional_targets": [
                    {"output_key": "cross_reference", "target_node_id": ids["cross_reference"]}
                ]
            }
        },
        {
            "id": ids["cross_reference"],
            "name": "🔄 Cross-Reference & Validate",
            "prompt": "Review findings from Angle A & B. Identify agreements/contradictions/gaps. Use web search to verify if needed.",
            "type": "llm_call",
            "routing_rules": {
                "default_target": ids["synthesize"],
                "conditional_targets": [
                    {"output_key": "revisit_A", "target_node_id": ids["search_A"]},
                    {"output_key": "revisit_B", "target_node_id": ids["search_B"]},
                    {"output_key": "synthesize", "target_node_id": ids["synthesize"]}
                ]
            }
        },
        {
            "id": ids["synthesize"],
            "name": "🧩 Synthesize Findings",
            "prompt": "Combine validated findings from research angles. Create concise summary for original goal.",
            "type": "llm_call",
            "routing_rules": {
                "default_target": ids["final_report"],
                "conditional_targets": [
                    {"output_key": "refine_synthesis", "target_node_id": ids["cross_reference"]},
                    {"output_key": "final_report", "target_node_id": ids["final_report"]}
                ]
            }
        },
        {
            "id": ids["final_report"],
            "name": "📄 Generate Final Report",
            "prompt": "Format synthesized findings into clear final report.",
            "type": "llm_call",
            "routing_rules": {
                "default_target": END_NODE_ID,
                "conditional_targets": [
                    {"output_key": "done", "target_node_id": END_NODE_ID}
                ]
            }
        }
    ]
    
    return nodes

def get_enhanced_hedge_fund_workflow():
    """
    Returns a sophisticated investment analysis workflow
    """
    ids = {name: f"ehf_node_{uuid.uuid4().hex[:4]}" for name in [
        "goal_risk", "planner", "macro", "sector", "company", "risk_assess", "strategist"
    ]}
    
    nodes = [
        {
            "id": ids["goal_risk"],
            "name": "🎯 Goal & Risk Profiler",
            "prompt": "Analyze investment goal from input. Clarify timeframe, expectations, infer risk tolerance (Conservative, Balanced, Aggressive). State profile.",
            "type": "llm_call",
            "routing_rules": {
                "default_target": ids["planner"],
                "conditional_targets": [
                    {"output_key": "plan_research", "target_node_id": ids["planner"]}
                ]
            }
        },
        {
            "id": ids["planner"],
            "name": "🗺️ Advanced Research Planner",
            "prompt": "Based on Goal/Risk, determine necessary research steps & sequence (Macro, Sector, Company). State plan. Decide FIRST step.",
            "type": "llm_call",
            "routing_rules": {
                "default_target": ids["risk_assess"],
                "conditional_targets": [
                    {"output_key": "research_macro", "target_node_id": ids["macro"]},
                    {"output_key": "research_sector", "target_node_id": ids["sector"]},
                    {"output_key": "research_company", "target_node_id": ids["company"]},
                    {"output_key": "go_strategy", "target_node_id": ids["strategist"]}
                ]
            }
        },
        {
            "id": ids["macro"],
            "name": "📈 Macro Researcher",
            "prompt": "Perform macro analysis relevant to Goal/Risk. Use web search if needed (GDP, rates, inflation). Summarize findings & impacts. Determine NEXT planned step.",
            "type": "llm_call",
            "routing_rules": {
                "default_target": ids["risk_assess"],
                "conditional_targets": [
                    {"output_key": "research_sector", "target_node_id": ids["sector"]},
                    {"output_key": "research_company", "target_node_id": ids["company"]},
                    {"output_key": "assess_risk", "target_node_id": ids["risk_assess"]}
                ]
            }
        },
        {
            "id": ids["sector"],
            "name": "🏭 Sector Researcher",
            "prompt": "Perform sector analysis relevant to Goal/Risk (guided by macro). Use web search if needed (trends/competitors). Summarize findings & impacts. Determine NEXT planned step.",
            "type": "llm_call",
            "routing_rules": {
                "default_target": ids["risk_assess"],
                "conditional_targets": [
                    {"output_key": "research_macro", "target_node_id": ids["macro"]},
                    {"output_key": "research_company", "target_node_id": ids["company"]},
                    {"output_key": "assess_risk", "target_node_id": ids["risk_assess"]}
                ]
            }
        },
        {
            "id": ids["company"],
            "name": "🏢 Company Researcher",
            "prompt": "Perform company analysis relevant to Goal/Risk (guided by macro/sector). Use web search if needed (news, financials). Summarize findings (valuation, risks) & impacts. Determine NEXT planned step.",
            "type": "llm_call",
            "routing_rules": {
                "default_target": ids["risk_assess"],
                "conditional_targets": [
                    {"output_key": "research_macro", "target_node_id": ids["macro"]},
                    {"output_key": "research_sector", "target_node_id": ids["sector"]},
                    {"output_key": "assess_risk", "target_node_id": ids["risk_assess"]}
                ]
            }
        },
        {
            "id": ids["risk_assess"],
            "name": "⚠️ Risk Assessor & Validator",
            "prompt": "Review ALL research findings against Goal/Risk. Identify key risks, inconsistencies, gaps. Use web search to verify if needed.",
            "type": "llm_call",
            "routing_rules": {
                "default_target": ids["strategist"],
                "conditional_targets": [
                    {"output_key": "revisit_macro", "target_node_id": ids["macro"]},
                    {"output_key": "revisit_sector", "target_node_id": ids["sector"]},
                    {"output_key": "revisit_company", "target_node_id": ids["company"]},
                    {"output_key": "create_strategy", "target_node_id": ids["strategist"]}
                ]
            }
        },
        {
            "id": ids["strategist"],
            "name": "💰 Portfolio Strategist",
            "prompt": "Synthesize validated research. Develop specific, diversified portfolio allocation strategy tailored to Goal/Risk. Justify strategy.",
            "type": "llm_call",
            "routing_rules": {
                "default_target": END_NODE_ID,
                "conditional_targets": [
                    {"output_key": "portfolio_ready", "target_node_id": END_NODE_ID}
                ]
            }
        }
    ]
    
    return nodes