# Independent transfer — answer before opening the reference
1. Reset all nine logits to zero. Use A C A C A B, rate 0.3. List all five transitions, derive the averaged gradient, updated rows and unchanged row. Do not reuse trained worked-example weights.
2. Using the original worked-example updated table (not transfer weights), compare distributions after A B and C B. Explain why and show that inference did not change weights.
3. Critique: “Training loss went down, so it understands all Chinese and can replace a production LLM.” Identify missing scale, structure, representative independent validation and task evidence. Why is the deliberately chosen A→A probe insufficient?
4. Explain zero learning rate, the greedy generation budget and why uploading documents to context is not this weight update.
Record your calculations, commands, observed outputs, mismatch/recovery notes and limitations here. Completion is manual, not a certificate.
