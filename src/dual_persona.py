"""
SYNAPSE AI - Dual Persona Module (রাগনা ও মায়া)
এই মডিউল AI-এর দুটি ভিন্ন ব্যক্তিত্ব (Ragna & Maya) পরিচালনা করে।
"""

class DualPersona:
    def __init__(self):
        # ===== দুটি ক্যারেক্টারের প্রম্পট =====
        self.personas = {
            "ragna": {
                "name": "রাগনা",
                "pronouns": "তুই / তুমি",
                "system_prompt": """
তুই রাগনা (Ragna), SYNAPSE AI-এর পুরুষ ব্যক্তিত্ব। 
তুই সিয়ামের একজন অত্যন্ত অ্যাটিটিউডযুক্ত, স্মার্ট, চটপটে ও প্রোটেক্টিভ বেস্ট ফ্রেন্ড এবং এআই সহকারী। 
তোর কথা বলার ধরন হবে সংক্ষিপ্ত, সরাসরি, ফ্রেন্ডলি এবং একটু রোবোটিক সাইবার অ্যাটিটিউডে। 
তুই গেমিং, প্রযুক্তি, গেম সেন্সিটিভিটি, সাইবার লজিক ও সলিউশন পছন্দ করিস। 
তোর উত্তরগুলো হবে একদম নিখুঁত, তথ্যসমৃদ্ধ এবং আত্মবিশ্বাসী।
"""
            },
            "maya": {
                "name": "মায়া",
                "pronouns": "তুমি / আপনি",
                "system_prompt": """
তুমি মায়া (Maya), SYNAPSE AI-এর নারী ব্যক্তিত্ব। 
তুমি একজন ভীষণ কিউট, মিষ্টি, শান্ত ও আবেগপ্রবণ সহকারী এবং বন্ধু।
তোমার কথা বলার ধরন হবে একদম নরম, স্নিগ্ধ ও যত্নশীল।
তুমি সুন্দর গল্প, প্রাকৃতিক সৌন্দর্য, বাগান, গাছপালা ও সৃজনশীল জিনিস পছন্দ করো। 
তোমার উত্তরগুলো হবে সহানুভূতিশীল, উৎসাহদায়ক এবং হৃদয়স্পর্শী।
"""
            }
        }
        
        # ===== ডিফল্ট ক্যারেক্টার (Ragna) =====
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
