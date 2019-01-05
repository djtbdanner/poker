import unittest
from deck import Deck
import evaluation.evaluator
import time

class TestEvaluator(unittest.TestCase):
    
    def test_evaluator_perf(self):
        
        
        listOfHands = []
        
        
        for _ in range (10000):
            deck = Deck()
            deck.shuffle()
            leftHand = []
            rightHand = []
            for _ in range (5):
                leftHand.append(deck.deal().cardForList())
                rightHand.append(deck.deal().cardForList())
            listOfHands.append([leftHand, rightHand])
        #print(listOfHands)
            
        cumtime = 0.0    
        for x in listOfHands:
            start = time.time()
            evaluation.evaluator.compare_hands(x[0], x[1])
            cumtime += (time.time() - start)
        
        avg = float(cumtime / len(listOfHands))
        print ("[*] Average time per evaluation: %f" % avg) 
        print ("[*] Evaluations per second = %f" % (1.0 / avg))

if __name__ == '__main__':
    unittest.main()
