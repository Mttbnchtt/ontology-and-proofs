## Summary
This folder contains scripts to facilitate the management of the ontology. Run the main.py file to execute one of the following operations:
- import proof steps;
- declare that given individiduals are all pairwise different;
- link steps to given proofs.


For help running the script type 
```
    $ python main.py -h
```
in the terminal. The terminal will display the following message:
```
    Execute some of the following:
                - import proof steps (import, --type step, --input, --output, --verbose <True, False>)
                - import allDifferent steps (import, --type allDifferent, --input, --output, --verbose <True, False>)
                - import link steps to proof (import, --type forProof, --input, --output, --verbose <True, False>)
```

### Import proof steps
1. Put the input file in the input folder. The input file should be a .txt file. It should contain exactly four resources in each line. For example, the following is an acceptable line:
```
    euclid:step1 euclid:triangle_ABC rdf:type euclid:Triangle
```
The script interprets the line above as saying the following:
```
    euclid:step1 a owl:NamedIndividual , 
            core:Proof_step ;
            core:proofStepStates [ a rdf:Statement ;
                                    rdf:subject euclid:triangle_ABC ;
                                    rdf:predicate rdf:type ;
                                    rdf:object euclid:Triangle ] .
```
2. Put the output file in the output folder. The output file ought to be an .rdf or .owl file. The script will open the file and append the above triples at the bottom of the file.
3. Run 
```
    $ python main.py import --type step --input <filename> --output <filename>
```
   
### Declare given individuals all different
1. Put the input file in the input folder. The input file should be a .txt file. It should contain exactly one resources in each line. For example, the following is an acceptable line:
```
    euclid:step1
    euclid:step2
```
The script interprets the line above as saying the following:
```
    [ a owl:AllDifferent ;
        owl:distinctMembers ( euclid:step1
        euclid:step2
        )
        ] .
```
2. Put the output file in the output folder. The output file ought to be an .rdf or .owl file. The script will open the file and append the above triples at the bottom of the file.
3. Run 
```
    $ python main.py import --type step --input <filename> --output <filename>
```

#### Link steps to proofs
1. Put the input file in the input folder. The input file should be a .txt file. It should contain exactly two resources in each line. For example, the following is an acceptable line:
```
    euclid:step1 euclid:proof_Euclid
```
The script interprets the line above as saying the following:
```
    euclid:step1 core:inProof euclid:proof_Euclid .
```
2. Put the output file in the output folder. The output file ought to be an .rdf or .owl file. The script will open the file and append the above triples at the bottom of the file.
3. Run 
```
    $ python main.py import --type forProof --input <filename> --output <filename>
```