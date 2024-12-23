tree = {
    "1": ["أهلا وسهلا بيك في فرنا بوت 🤖! هاني هنا باش نعاونك تلقى فرص تدريب 📚 وخدمة في فرنانة. نقدر نعطيك آخر الأخبار على التدريبات والفرص المهنية. إختار شنوا تحب تعرف أكثر 🤔 وأنا في الخدمة! 😊 ","2", "3", "4"],

    "2": ["تحب تعرف على فرص الخدمة؟ اكتبلنا شويا على خبرتك والشغل إلي تحب تلقاه.", "2,1", "2,2"],
    "3": ["تحب تعرف على الدورات التدريبية المتاحة؟ قولنا شنوة مجالات التدريب إلي تهمك.", "3,1", "3,2", "3,3"],
    "4": ["للمساعدة أو الإستفسارات اتصل بينا.", "4,1"],

    # Detailed options for job search
    "2,1": "هل تريد مساعدة في كيفية كتابة السيرة الذاتية أو التحضير لمقابلة؟",
    "2,2": "أنا بش نبعثلك آخر العروض حسب المعطيات إلي دخلتها. إستنى شوية.",

    # Detailed options for training
    "3,1": "عندنا دورات في تكنولوجيا المعلومات والبرمجة. تحب تسجل؟",
    "3,2": "في تدريبات في التصميم والفنون. تحب تعرف أكثر؟",
    "3,3": "لو تحب تدريب في إدارة الأعمال، عنا خيارات متعددة. اختار اللي يعجبك.",

    # Support
    "4,1": "12 345 678"
}

# Example usage:
current_key = "1"
print(tree[current_key][0])  # Display the welcome message and options

# Suppose the user selects option 2 (Job search)
current_key = "2"
print(tree[current_key][0])  # Display the job search intro

# User inputs their interest in IT jobs, which triggers the next response
current_key = "2,2"
print(tree[current_key])  # Display the response for IT job postings
