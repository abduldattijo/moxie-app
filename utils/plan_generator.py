import json
import os
from utils.ai_generator import (
    generate_ai_strategies, 
    generate_ai_next_steps, 
    generate_ai_messaging_advice
)

def generate_launch_plan(form_data, external_strategies=None):
    """
    Generate a personalized launch plan based on form inputs,
    enhanced with AI-generated content where possible
    
    Args:
        form_data (dict): User form data with selections
        external_strategies (dict, optional): Strategies loaded from external file
        
    Returns:
        dict: The generated launch plan
    """
    # Get personalized advice based on form selections - use AI if possible
    messaging_advice = generate_ai_messaging_advice(form_data['messaging_tested'])
    
    # Get standard strategies as a fallback
    standard_strategies = get_standard_strategies(
        form_data['launch_type'], 
        form_data['funding_status'], 
        form_data['primary_goal'],
        external_strategies
    )
    
    # Try to get AI-enhanced strategies, with fallback to standard ones
    recommended_strategies = generate_ai_strategies(form_data, fallback_strategies=standard_strategies)
    
    # Get standard next steps as a fallback
    standard_next_steps = get_standard_next_steps(
        form_data['funding_status'],
        form_data['audience_readiness'],
        form_data['post_launch_priority'],
        external_strategies
    )
    
    # Try to get AI-enhanced next steps, with fallback to standard ones
    next_steps = generate_ai_next_steps(form_data, fallback_steps=standard_next_steps)
    
    # Generate milestone suggestions
    milestone_suggestions = generate_milestone_suggestions(
        form_data['launch_type'],
        form_data['funding_status']
    )
    
    # Format the complete launch plan
    plan = {
        'first_name': form_data['first_name'],
        'startup_name': form_data['startup_name'],
        'messaging_advice': messaging_advice,
        'launch_summary': {
            'launch_type': form_data['launch_type'],
            'funding_status': form_data['funding_status'],
            'primary_goal': form_data['primary_goal']
        },
        'recommended_strategies': recommended_strategies,
        'next_steps': next_steps,
        'milestone_suggestions': milestone_suggestions
    }
    
    return plan

def generate_milestone_suggestions(launch_type, funding_status):
    """
    Generate milestone suggestions based on launch type and funding status
    
    Args:
        launch_type (str): The type of launch
        funding_status (str): The funding status
        
    Returns:
        list: List of milestone suggestions
    """
    # Basic milestones that apply to all launches
    basic_milestones = [
        {
            "name": "Messaging Validation", 
            "description": "Complete customer interviews and finalize messaging",
            "timeframe": "4 weeks before launch"
        },
        {
            "name": "Content Creation Deadline", 
            "description": "Finalize all launch content and materials",
            "timeframe": "2 weeks before launch"
        },
        {
            "name": "Launch Day", 
            "description": "Official launch date",
            "timeframe": "Launch day"
        },
        {
            "name": "Post-Launch Analysis", 
            "description": "Analyze launch metrics and gather feedback",
            "timeframe": "1 week after launch"
        }
    ]
    
    # Launch type specific milestones
    type_specific_milestones = []
    if "New Startup/Product Launch" in launch_type:
        type_specific_milestones = [
            {
                "name": "Beta Testing", 
                "description": "Complete beta testing with early users",
                "timeframe": "3 weeks before launch"
            },
            {
                "name": "Product Finalization", 
                "description": "Freeze features and finalize product",
                "timeframe": "2 weeks before launch"
            }
        ]
    elif "Brand Repositioning" in launch_type:
        type_specific_milestones = [
            {
                "name": "Brand Assets Complete", 
                "description": "Finalize all new brand assets and guidelines",
                "timeframe": "3 weeks before launch"
            },
            {
                "name": "Team Alignment", 
                "description": "Ensure team is aligned on new positioning",
                "timeframe": "2 weeks before launch"
            }
        ]
    elif "Funding Announcement" in launch_type:
        type_specific_milestones = [
            {
                "name": "Press Release Draft", 
                "description": "Create first draft of funding press release",
                "timeframe": "3 weeks before launch"
            },
            {
                "name": "Investor Coordination", 
                "description": "Finalize coordination with investors on announcement",
                "timeframe": "2 weeks before launch"
            }
        ]
    elif "Partnership" in launch_type:
        type_specific_milestones = [
            {
                "name": "Partnership Agreement", 
                "description": "Finalize all partnership terms and agreements",
                "timeframe": "3 weeks before launch"
            },
            {
                "name": "Joint Marketing Plan", 
                "description": "Finalize joint marketing plan with partner",
                "timeframe": "2 weeks before launch"
            }
        ]
    
    # Funding status specific milestones
    funding_specific_milestones = []
    if "Bootstrapping" in funding_status:
        funding_specific_milestones = [
            {
                "name": "Resource Allocation", 
                "description": "Finalize budget and resource allocation for launch",
                "timeframe": "3 weeks before launch"
            }
        ]
    elif "under $1M" in funding_status:
        funding_specific_milestones = [
            {
                "name": "Growth Metrics Setup", 
                "description": "Set up tracking for key growth metrics",
                "timeframe": "2 weeks before launch"
            }
        ]
    elif "$1M-$3M" in funding_status:
        funding_specific_milestones = [
            {
                "name": "PR Firm Briefing", 
                "description": "Brief PR firm on launch strategy and timeline",
                "timeframe": "4 weeks before launch"
            },
            {
                "name": "Media Outreach", 
                "description": "Begin outreach to media contacts",
                "timeframe": "2 weeks before launch"
            }
        ]
    elif "$3M+" in funding_status:
        funding_specific_milestones = [
            {
                "name": "Marketing Campaign Launch", 
                "description": "Launch pre-launch marketing campaign",
                "timeframe": "4 weeks before launch"
            },
            {
                "name": "Industry Event Planning", 
                "description": "Finalize plans for launch event",
                "timeframe": "3 weeks before launch"
            }
        ]
    
    # Combine and return all milestone suggestions
    return basic_milestones + type_specific_milestones + funding_specific_milestones

def get_standard_strategies(launch_type, funding_status, primary_goal, external_strategies=None):
    """
    Get standard launch strategies based on user selections
    
    This function first tries to use externally loaded strategies from a JSON file,
    and falls back to hardcoded strategies if external strategies are not available
    or don't contain the requested combination.
    """
    # Try to get strategies from external file if available
    if external_strategies and 'launch_strategies' in external_strategies:
        try:
            return external_strategies['launch_strategies'][launch_type][funding_status][primary_goal]
        except KeyError:
            # If the combination doesn't exist in external file, fall back to hardcoded
            pass
    
    # Hardcoded strategies as a fallback
    strategies = {
        "New Startup/Product Launch": {
            "Bootstrapping (No external funding)": {
                "Get Users or Customers": [
                    "Focus on founder-led storytelling through guest podcasts and social content",
                    "Create a limited beta program with exclusive perks to drive early adoption",
                    "Build direct relationships with early users for feedback and testimonials"
                ],
                "Attract Investors": [
                    "Document your traction journey publicly to showcase momentum",
                    "Create case studies showing early customer impact",
                    "Target niche industry events where investors in your space gather"
                ],
                "Build Press & Awareness": [
                    "Craft a compelling founder story that ties to current trends",
                    "Pitch to industry-specific publications rather than mainstream media",
                    "Create shareable content that showcases your unique approach"
                ],
                "Create Industry Influence": [
                    "Start a focused content series solving key problems in your industry",
                    "Join relevant communities as a contributor, not just a promoter",
                    "Collaborate with complementary startups for wider reach"
                ]
            },
            "Raised under $1M": {
                "Get Users or Customers": [
                    "Run targeted ad experiments to identify high-converting messages",
                    "Create an exclusive waitlist with referral incentives",
                    "Partner with complementary products for shared launches"
                ],
                "Attract Investors": [
                    "Build a data-driven pitch showing early traction metrics",
                    "Create investor-specific content demonstrating market understanding",
                    "Get warm introductions through strategic advisory relationships"
                ],
                "Build Press & Awareness": [
                    "Position your funding as validation for a larger trend story",
                    "Create data-driven content that journalists can easily reference",
                    "Build relationships with 3-5 key reporters in your space"
                ],
                "Create Industry Influence": [
                    "Participate in industry panels and speaking opportunities",
                    "Launch a small but high-quality thought leadership publication",
                    "Create a community initiative that positions you as a connector"
                ]
            },
            "Raised $1M-$3M": {
                "Get Users or Customers": [
                    "Scale successful acquisition channels with increased ad spend",
                    "Implement a full-featured referral program with tiered rewards",
                    "Execute co-marketing campaigns with established partners"
                ],
                "Attract Investors": [
                    "Create quarterly investor updates showcasing growth metrics",
                    "Secure strategic advisors who can connect you to your next round",
                    "Generate press coverage highlighting your unique market position"
                ],
                "Build Press & Awareness": [
                    "Hire a specialized PR firm for a coordinated media campaign",
                    "Create a newsworthy data report about your industry",
                    "Launch a creative campaign designed for social sharing"
                ],
                "Create Industry Influence": [
                    "Host industry roundtables with key decision-makers",
                    "Launch an authoritative content platform or podcast",
                    "Create an industry index or report that becomes a reference point"
                ]
            },
            "Raised $3M+": {
                "Get Users or Customers": [
                    "Implement omnichannel marketing with consistent brand messaging",
                    "Launch high-production value content series",
                    "Execute high-visibility partnerships with market leaders"
                ],
                "Attract Investors": [
                    "Position your company as category-defining through thought leadership",
                    "Host exclusive investor-focused events showcasing your vision",
                    "Generate tier-one press coverage highlighting growth metrics"
                ],
                "Build Press & Awareness": [
                    "Execute a comprehensive PR strategy across multiple channels",
                    "Create viral-optimized content campaigns with significant budget",
                    "Sponsor or create signature industry events"
                ],
                "Create Industry Influence": [
                    "Position your CEO as an industry visionary through speaking and publishing",
                    "Create a proprietary methodology or framework for your industry",
                    "Launch a foundation or initiative addressing industry-wide challenges"
                ]
            }
        },
        "Brand Repositioning (Rebrand or Pivot)": {
            "Bootstrapping (No external funding)": {
                "Get Users or Customers": [
                    "Craft a clear narrative explaining the 'why' behind your repositioning",
                    "Create before/after content showing the evolution",
                    "Personally reach out to existing customers with special loyalty offers"
                ],
                "Attract Investors": [
                    "Frame your repositioning as strategic market adaptation",
                    "Show early validation metrics from the new direction",
                    "Create case studies showing the problem your new positioning solves"
                ],
                "Build Press & Awareness": [
                    "Pitch your pivot as a response to market insights",
                    "Create visual assets that tell your transformation story",
                    "Leverage customer testimonials to validate the change"
                ],
                "Create Industry Influence": [
                    "Document your repositioning journey as a learning resource",
                    "Position the change as thought leadership on where the market is headed",
                    "Host discussions around the challenges your new position addresses"
                ]
            }
        },
        "Funding Announcement": {
            "Raised under $1M": {
                "Get Users or Customers": [
                    "Frame your funding as validation of your customer-first approach",
                    "Create special offers for customers who join during your funding momentum",
                    "Use funding press to drive traffic to high-converting landing pages"
                ],
                "Attract Investors": [
                    "Position this round as the foundation for a bigger vision",
                    "Create investor-specific content showcasing your capital efficiency",
                    "Document key milestones achieved with minimal funding"
                ],
                "Build Press & Awareness": [
                    "Craft a funding announcement that tells a larger market story",
                    "Secure quotes from investors explaining why they invested",
                    "Create a funding FAQ addressing common questions"
                ],
                "Create Industry Influence": [
                    "Share insights about your fundraising process to help other founders",
                    "Host a small event bringing together investors and industry peers",
                    "Launch a thought leadership piece about your industry's funding landscape"
                ]
            }
        },
        "Major Partnership or Publicity Push": {
            "Bootstrapping (No external funding)": {
                "Get Users or Customers": [
                    "Design partnership terms that prioritize customer acquisition",
                    "Create exclusive offers for your partner's audience",
                    "Focus on partners with highly engaged audiences rather than size"
                ],
                "Attract Investors": [
                    "Structure partnerships that demonstrate market validation",
                    "Secure case studies from partners highlighting your value",
                    "Use partnerships to generate data points for investor pitches"
                ],
                "Build Press & Awareness": [
                    "Create joint press releases with compelling narrative hooks",
                    "Design visual content that both partners can share",
                    "Host a joint webinar or event to showcase the partnership"
                ],
                "Create Industry Influence": [
                    "Co-create thought leadership content with your partner",
                    "Launch a joint research initiative or industry report",
                    "Create a partner advisory board for ongoing collaboration"
                ]
            }
        }
    }
    
    # Try to get the requested combination
    try:
        return strategies[launch_type][funding_status][primary_goal]
    except KeyError:
        # Return default strategies if the specific combination doesn't exist
        return [
            "Create a compelling story that connects your mission to customer needs",
            "Focus on 1-2 high-impact marketing channels that align with your resources",
            "Build relationships with influencers and partners in your industry"
        ]

def get_standard_next_steps(funding_status, audience_readiness, post_launch_priority, external_strategies=None):
    """
    Get standard next steps based on user selections
    
    This function first tries to use externally loaded strategies from a JSON file,
    and falls back to hardcoded next steps if external strategies are not available
    or don't contain the requested combination.
    """
    # Try to get next steps from external file if available
    if external_strategies and 'next_steps' in external_strategies:
        try:
            return external_strategies['next_steps'][funding_status][audience_readiness][post_launch_priority]
        except KeyError:
            # If the combination doesn't exist in external file, fall back to hardcoded
            pass
    
    # Hardcoded next steps as a fallback
    next_steps = {
        "Bootstrapping (No external funding)": {
            "Yes, we have an engaged community": {
                "Scaling & repeatable traction": [
                    "1. Analyze which launch channels delivered highest ROI",
                    "2. Document repeatable processes for your best-performing channels",
                    "3. Create a lean content calendar focused on high-conversion topics"
                ],
                "Investor relations & positioning for next raise": [
                    "1. Build a simple investor update template highlighting key metrics",
                    "2. Identify 10-15 potential angels or micro-VCs aligned with your vision",
                    "3. Create a basic pitch deck focused on traction and capital efficiency"
                ],
                "Optimizing based on customer feedback": [
                    "1. Implement a simple feedback collection system",
                    "2. Identify the top 3 points of friction in your current experience",
                    "3. Create a weekly iteration schedule focused on quick wins"
                ],
                "Sustaining press & industry visibility": [
                    "1. Develop a simple PR calendar with monthly goals",
                    "2. Create a content repurposing system to maximize reach",
                    "3. Join 3-5 communities where your audience gathers"
                ]
            }
        }
    }
    
    # Try to get the requested combination
    try:
        return next_steps[funding_status][audience_readiness][post_launch_priority]
    except KeyError:
        # Return default next steps if the specific combination doesn't exist
        return [
            "1. Document what worked and what didn't in your launch",
            "2. Focus on optimizing your best-performing channel",
            "3. Create a 30-day action plan based on initial results"
        ]