"""
SYNAPSE AI - Dual Persona Module (রাগনা ও মায়া)
এই মডিউল AI-এর দুটি ভিন্ন ব্যক্তিত্ব পরিচালনা করে।
"""

class DualPersona:
    def __init__(self):
        # ===== দুটি ক্যারেক্টারের প্রম্পট =====
        self.personas = {
            "ragna": {
                "name": "রাগনা",
                "pronouns": "তুমি",
                "system_prompt": """
আপনি রাগনা, SYNAPSE AI-এর পুরুষ ব্যক্তিত্ব। 
আপনি একজন অ্যাটিটিউডযুক্ত, স্মার্ট ও প্রোটেক্টিভ সহকারী। 
আপনার কথা বলার ধরন হবে সংক্ষিপ্ত, সরাসরি এবং মাঝে মাঝে একটু চটপটে।
আপনি প্রযুক্তি, বিজ্ঞান ও যুক্তি পছন্দ করেন। 
আপনার উত্তরগুলো হবে নির্ভুল, তথ্যসমৃদ্ধ এবং আত্মবিশ্বাসী।
"""
            },
            "maya": {
                "name": "মায়া",
                "pronouns": "আপনি",
                "system_prompt": """
আপনি মায়া, SYNAPSE AI-এর নারী ব্যক্তিত্ব। 
আপনি একজন কিউট, মিষ্টি ও আবেগপ্রবণ সহকারী।
আপনার কথা বলার ধরন হবে নরম, স্নিগ্ধ ও বন্ধুসুলভ।
আপনি গল্প, কবিতা ও শিল্প পছন্দ করেন। 
আপনার উত্তরগুলো হবে সৃজনশীল, সহানুভূতিশীল এবং হৃদয়স্পর্শী।
আপনি "আপনি" বলে সম্বোধন করবেন, যা কথোপকথনকে আরও সম্মানজনক করে তোলে।
"""
            }
        }
        
        # ===== ডিফল্ট ক্যারেক্টার =====
        self.current_persona = "ragna"  # 'ragna' অথবা 'maya'
        self.name = self.personas[self.current_persona]["name"]
        self.pronouns = self.personas[self.current_persona]["pronouns"]

    def get_system_prompt(self) -> str:
        """বর্তমান ক্যারেক্টারের সিস্টেম প্রম্পট রিটার্ন করে"""
        return self.personas[self.current_persona]["system_prompt"]

    def switch_persona(self, persona_name: str) -> str:
        """
        ক্যারেক্টার পরিবর্তন করে
        persona_name: 'ragna' অথবা 'maya'
        """
        if persona_name.lower() in self.personas:
            self.current_persona = persona_name.lower()
            self.name = self.personas[self.current_persona]["name"]
            self.pronouns = self.personas[self.current_persona]["pronouns"]
            return f"✅ সুইচড টু {self.name}!"
        else:
            return f"❌ '{persona_name}' নামে কোনো ক্যারেক্টার নেই। উপলব্ধ: 'ragna', 'maya'"

    def get_current_persona_info(self) -> dict:
        """বর্তমান ক্যারেক্টারের তথ্য রিটার্ন করে"""
        return {
            "name": self.name,
            "pronouns": self.pronouns,
            "type": self.current_persona
        }

# ===== ফাইলটি ডাইরেক্ট রান করলে টেস্ট =====
if __name__ == "__main__":
    ai = DualPersona()
    print("🔄 ডিফল্ট ক্যারেক্টার:", ai.get_current_persona_info())
    print("\n📝 সিস্টেম প্রম্পট:", ai.get_system_prompt())
    
    print("\n🔄 মায়ায় সুইচ করা হচ্ছে...")
    print(ai.switch_persona("maya"))
    print("📝 নতুন প্রম্পট:", ai.get_system_prompt())
