import json
import random

def combine_data(faq_file, course_file, output_file):
    with open(faq_file, 'r') as f:
        faqs = json.load(f)

    with open(course_file, 'r') as f:
        courses = json.load(f)

    qa_pairs = []

    # Add FAQs
    for faq in faqs:
        qa_pairs.append({
            "text": f"Question: {faq['question']}\nAnswer: {faq['answer']}"
        })

    # Add course descriptions as Q&A pairs
    for course in courses:
        qa_pairs.append({
            "text": f"Question: What is {course['title']}?\nAnswer: {course['description']}"
        })

    # Shuffle the data
    random.shuffle(qa_pairs)

    # Save to JSON
    with open(output_file, 'w') as f:
        json.dump(qa_pairs, f, indent=4)

def split_data(input_file, train_file, val_file, split_ratio=0.8):
    with open(input_file, 'r') as f:
        data = json.load(f)

    random.shuffle(data)
    split_point = int(len(data) * split_ratio)
    train_data = data[:split_point]
    val_data = data[split_point:]

    with open(train_file, 'w') as f:
        json.dump(train_data, f, indent=4)

    with open(val_file, 'w') as f:
        json.dump(val_data, f, indent=4)

def main():
    combine_data('faqs.json', 'courses.json', 'combined.json')
    split_data('combined.json', 'train_split.json', 'val_split.json')

if __name__ == "__main__":
    main()
