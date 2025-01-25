from transformers import AutoTokenizer, AutoModelForCausalLM

def main():
    # Path to your locally saved TinyLlama model
    model_path = "path/to/tinyllama"

    # Load the tokenizer and model
    print("Loading TinyLlama model...")
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForCausalLM.from_pretrained(model_path)

    print("TinyLlama is ready!")
    print("Type 'exit' to quit.")

    while True:
        user_input = input("\nYou: ")
        if user_input.lower() == "exit":
            print("Goodbye!")
            break

        # Generate response
        inputs = tokenizer(user_input, return_tensors="pt")
        outputs = model.generate(inputs["input_ids"], max_length=150)
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)

        print(f"TinyLlama: {response}")

if __name__ == "__main__":
    main()
    