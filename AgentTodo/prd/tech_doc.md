NLP for:
    - what is the intent?(add, remove or show) : intent recognition 
    - what exactly needs to be updated?(task name) : entity extraction
        - used [sPacy](https://github.com/explosion/spaCy) 


sPacy NLP Debugging Info:

    You: Can you add groceries to my list?

    --- Debugging: spaCy Doc Tokens ---
    Text: can, Lemma: can, POS: AUX, Dep: aux, Head: add
    Text: you, Lemma: you, POS: PRON, Dep: nsubj, Head: add
    Text: add, Lemma: **add**, POS: **VERB**, Dep: ROOT, Head: add
    Text: groceries, Lemma: **grocery**, POS: **NOUN**, Dep: dobj, Head: add
    Text: to, Lemma: to, POS: ADP, Dep: prep, Head: add
    Text: my, Lemma: my, POS: PRON, Dep: poss, Head: list
    Text: list, Lemma: list, POS: NOUN, Dep: pobj, Head: to
    Text: ?, Lemma: ?, POS: PUNCT, Dep: punct, Head: add
    --- End of Debugging ---


    --- Debugging: Noun Chunks ---
    Text: you, Root: you, Root Dep: nsubj
    Text: groceries, Root: groceries, Root Dep: dobj
    Text: my list, Root: list, Root Dep: pobj
    --- End of Debugging ---

    AI: Task 'groceries' added to your list!



Below examples doesn't work with spacy nlp:

      * You: add organize wardrobe to the list    

        --- Debugging: spaCy Doc Tokens ---
        Text: add, Lemma: add, POS: VERB, Dep: ROOT, Head: add
        Text: organize, Lemma: organize, POS: VERB, Dep: xcomp, Head: add
        Text: wardrobe, Lemma: wardrobe, POS: NOUN, Dep: dobj, Head: organize
        Text: to, Lemma: to, POS: ADP, Dep: prep, Head: organize
        Text: the, Lemma: the, POS: DET, Dep: det, Head: list
        Text: list, Lemma: list, POS: NOUN, Dep: pobj, Head: to
        --- End of Debugging ---


        --- Debugging: Noun Chunks ---
        Text: wardrobe, Root: wardrobe, Root Dep: dobj
        Text: the list, Root: list, Root Dep: pobj
        --- End of Debugging ---

        AI: Task 'wardrobe' added to your list!

      *   
