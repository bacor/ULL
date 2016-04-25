
# Some random notes.

Suppose your input is
```
I am happy
I drink a cup of coffee
```
These are your first two sequences, and you want to reverse this. How do you do this? Well, you have some MxM matrix (e.g. M=100). The idea: assign an integer to every word
```
1 2  3
I am happy

1 3     4 5   6  7
I drink a cup of coffee
```

Then the matrix looks like
```
[[0 1 2 0 0 0 0 0 ...
  0 3 4 5 6 7 0 0 ...]]
```

So you use a masking matrix
```
[[1 1 1 0 0 0 0 0 ...
  1 1 1 1 1 1 0 0 ...]]
```

But note that in your actual position, for every input you have a vector. So the numbers we just used are actually indices for the wordvectors. 

End of sentence is just another word such as `<EOS>`. Do create this since you don't know how your sentence will end (dot, question mark, exlamation bar etc). As for indexing, people usually use 0 for the begin of the sentence and 1 for the end of the sentence.