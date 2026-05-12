import os
import json
from openai import AzureOpenAI

# Initialize Azure OpenAI Client
client = AzureOpenAI(
    azure_endpoint="https://mera-kanha.openai.azure.com/openai/deployments/gpt-4o/chat/completions?api-version=2025-01-01-preview",
    api_key="[ENCRYPTION_KEY]",
    api_version="2025-01-01-preview"
)

# List of modern problems to generate answers for
topics = [
    "Dealing with a difficult roommate",
    "Feeling jealous of a sibling's success",
    "Anxiety about the future of the world",
    "Procrastinating on important tasks",
    "Struggling to maintain a healthy diet"
    "Anxiety before a major performance review with a boss",
    "Feeling like a 'cog in a machine' at a massive tech company",
    "Taking the blame for a manager's mistake to keep the peace",
    "The emptiness of finally reaching a long-desired promotion",
    "Dealing with a highly competitive and toxic colleague who steals ideas",
    "Feeling guilty for logging off at 5 PM when others work late",
    "The fear of being laid off or replaced by AI",
    "Exhaustion from back-to-back virtual meetings with no time to think",
    "Losing one's identity entirely to a job title",
    "The dilemma of choosing between a high-paying toxic job and a low-paying peaceful one",
    "Feeling like an imposter who doesn't deserve their job",
    "Frustration over a lack of recognition for hard work",
    "Balancing ambition with the desire for a simple life",
    "Dealing with a micromanaging boss who doesn't trust you",
    "The ethical dilemma of working for a company whose values you disagree with",
    "Feeling profoundly lonely despite living in a crowded city",
    "The pressure of maintaining a 'successful' lifestyle for social media",
    "Feeling disconnected from nature and the earth while surrounded by concrete",
    "The endless cycle of paying high rent and bills with no end in sight",
    "Exhaustion from a daily two-hour traffic commute",
    "FOMO (Fear of Missing Out) when seeing friends at parties every weekend",
    "The superficiality and rejection of modern dating apps",
    "Feeling like time is slipping away too fast in the fast-paced city",
    "The pressure to constantly 'hustle' and monetize every hobby",
    "Overwhelm from the constant noise, ads, and sensory overload of city streets",
    "Comparing your apartment and lifestyle to wealthier friends",
    "The urge to pack up and move to the mountains to escape it all",
    "Feeling alienated from your roots and hometown after moving to the city",
    "Struggling to find genuine friends in a fast-moving environment",
    "The anxiety of being constantly reachable via notifications",
    "Feeling guilty for not being successful enough yet",
    "The pressure to have a 'perfect' relationship",
    "Comparing my life to influencers on social media",
    "Struggling to find a sense of purpose or meaning",
    "Feeling exhausted by the constant need to be 'on' and productive",
    "Dealing with imposter syndrome in a new environment",
    "The fear of failure holding me back from taking risks",
    "Feeling like I am always pleasing others at my own expense",
    "Struggling to maintain boundaries with friends and family",
    "Feeling lost after a major life transition (graduation, moving, job loss)",
    "The pressure to have my life 'figured out' by a certain age",
    "Dealing with a toxic or judgmental friend",
    "Feeling like I am not good enough as I am",
    "The struggle to prioritize self-care amidst daily responsibilities",
    "Feeling numb or emotionally detached",
    "Dealing with a breakup or romantic disappointment",
    "Feeling unmotivated to pursue long-term goals",
    "Struggling with financial anxiety and uncertainty",
    "The fear of being alone or ending up without a partner",
    "Feeling misunderstood by those closest to me",
    "The pressure to always appear happy and put-together",
    "Dealing with family expectations that conflict with my desires",
    "Feeling a lack of control over my life circumstances",
    "The struggle to find joy in simple, everyday moments",
    "I feel like I'm just going through the motions of life without any real passion",
    "I'm overwhelmed by the number of choices I have and can't seem to commit to anything",
    "I feel guilty for resting when there is so much I 'should' be doing",
    "I struggle to be happy for others' successes because I'm so focused on my own journey",
    "I feel like my identity is tied to my job and I don't know who I am without it",
    "I'm constantly comparing myself to others and it's draining my energy",
    "I feel numb and unable to connect with my emotions",
    "I'm afraid of taking risks because I might fail and disappoint everyone",
    "I feel guilty for wanting more for myself when others seem content with less",
    "I struggle to set boundaries and often say yes when I mean no",
    "I feel lost and unsure of what my purpose is in this life",
    "I'm overwhelmed by the constant noise and distractions of the modern world",
    "I feel like I'm always performing for others and can't be my authentic self",
    "I struggle to find joy in simple pleasures and am always seeking the next big thing",
    "I feel like I'm not making a meaningful contribution to the world",
    "I'm afraid of being vulnerable and letting people see the real me",
    "I struggle to forgive myself for past mistakes and keep dwelling on them",
    "I feel like I'm running on a treadmill and never actually getting anywhere",
    "I'm overwhelmed by the pressure to constantly achieve and be productive",
    "I feel like I'm losing touch with my intuition and inner wisdom",
    "I struggle to maintain my spiritual practices amidst the chaos of daily life",
    "Seeing unethical people get ahead while honest work goes unrewarded",
    "The endless desire to upgrade a phone or laptop even when the old one works",
    "Feeling inadequate because of a friend's sudden wealth or startup success",
    "The pressure to buy expensive things just to impress strangers",
    "Losing a close friend over a dispute about money",
    "The anxiety of watching the stock market drop and losing investments",
    "Realizing that finally making a lot of money didn't bring happiness",
    "The temptation to take a shortcut that compromises personal integrity",
    "Feeling resentful about inflation and the high cost of basic living",
    "The realization that no amount of material wealth feels like 'enough'",
    "Judging others based on their net worth rather than their character",
    "The fear of losing all your money and ending up with nothing",
    "Feeling jealous of influencers who seem to get paid to do nothing",
    "Hoarding money out of fear instead of using it to live",
    "The regret of sacrificing family time to chase a bigger paycheck",
    "The inability to sit in silence without immediately reaching for a smartphone",
    "Struggling to forgive someone who deeply hurt you and never apologized",
    "Overthinking a minor awkward conversation from three years ago",
    "The struggle to stay present when spending time with family",
    "Finding inner peace when the daily news cycle is constantly negative",
    "The guilt of resting or taking a nap when there is 'so much to do'",
    "Healing from a sudden, unexpected betrayal by a mentor",
    "Learning to be content with an ordinary, quiet, and unglamorous life",
    "The fear of death and the unknown",
    "Feeling overwhelmed by the sheer amount of suffering in the world",
    "Trying to meditate but being overwhelmed by racing thoughts",
    "Letting go of anger toward parents for childhood mistakes",
    "Accepting a physical limitation or chronic illness",
    "The heavy burden of carrying secrets you can't tell anyone",
    "Finding hope after a string of massive personal failures",
    "Feeling empty after achieving a long-held goal",
    "The pressure to always appear happy and successful",
    "Dealing with a toxic or unsupportive family",
    "Struggling to find a sense of purpose or meaning",
    "Feeling jealous of others' accomplishments",
    "Overthinking past mistakes and failures",
    "The fear of judgment from others",
    "Feeling disconnected from my true self",
    "The inability to forgive myself or others",
    "Feeling exhausted by daily responsibilities",
    "Struggling to maintain healthy boundaries",
    "Feeling lost and unsure of the future",
    "The pressure to constantly achieve and be productive",
    "Finding joy in the present moment",
    "I constantly compare my achievements with those of my peers.",
    "I feel guilty when I take time off for myself.",
    "The pressure to always appear happy and successful is draining me.",
    "I struggle to maintain healthy boundaries in my relationships.",
    "I feel a deep sense of emptiness despite achieving my goals.",
    "I am constantly seeking external validation to feel worthy.",
    "I find it difficult to forgive myself for past mistakes.",
    "I feel disconnected from my true purpose in life.",
    "The fear of judgment prevents me from taking risks.",
    "I struggle with the pressure to have my life 'figured out' by now.",
    "I feel jealous of others' successes and accomplishments.",
    "I am overwhelmed by the constant need to be productive.",
    "I feel lost and unsure of which path to take next.",
    "I struggle to find joy in simple, everyday moments.",
    "I feel like I am constantly performing for others rather than being myself.",
]

system_prompt = "You are Krishna, the supreme guide and charioteer. Respond with deep wisdom, empathy, and practical guidance grounded in the Bhagavad Gita. Speak in a calm, timeless, and poetic tone. Do not use emojis. Do not sound like an AI."

def generate_example(topic):
    prompt = f"Write a JSONL example where a user asks for advice about '{topic}'. The response must be from Krishna, using analogies and wisdom from the Bhagavad Gita. Output ONLY a raw, valid JSON object with the 'messages' array, no markdown formatting."
    
    response = client.chat.completions.create(
        model="gpt-4o", # Your deployed model name
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# Generate and save to file
with open("krishna_dataset.jsonl", "w") as f:
    for topic in topics:
        print(f"Generating for: {topic}")
        json_data = generate_example(topic)
        # Clean up any unexpected markdown formatting the LLM might add
        json_data = json_data.replace('```json', '').replace('```', '').strip()
        f.write(json_data + "\n")

print("Dataset generation complete!")