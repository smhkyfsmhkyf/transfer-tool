Structure of references (as of 2025)
(i.e., line, nozzle, valve, etc all reference node)

                                                                                                                         node
      _______________________________________________________________________|___________________________________________________________________
      line                 nozzle                   tankreturn               pump                                 split                                                                               valve          
         |                           |                                |                                 |                        ___________|___________________                  _____________________|______________________________
   excelData       excelData              excelData                excelData               main      excelData        valve2                  valve2               excelData                             valve3
         |                          |                               |                                  |                                                  |                   |                               |                            |                   _______________\_________________________
    main                   main                      main                         main                                          main       excelData                 excelData             main              main             excelData            docwriter
                                                                                                                                                                                 |                                  |                                                                           |                               |
                                                                                                                                                                              main                          main                                                                  main                       main
      
      ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
      pit
       |
  excelData
       |
    main
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    graph
        |
     main
     ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from utils.pit import Pit

node 
   ->line
   ->nozzle
   ->pump
   ->split
      ->main
   ->tankreturn
   ->valve
       ->valve2
       ->valve3 (-->main)
           ->excelData
               ->main
           ->docwriter
               ->main
graph
   ->main


~~~~~~~~
(
main uses:
-docwriter
-excelData
-graph
-valve3
-split
)
~~~~~~~~~~~~~~~~~~~~
Order of operations in start-up

1. node 
2. valve
3. split
4. valve2
5. valve3
6. line
7. docwriter
8. nozzle
9. pump
10. tankreturn*
11. pit*
12. excelData
13. main
 
*Order may be switched. 
