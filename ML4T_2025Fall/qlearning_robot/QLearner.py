""""""  		  	   		 	 	 		  		  		    	 		 		   		 		  
"""  		  	   		 	 	 		  		  		    	 		 		   		 		  
Template for implementing QLearner  (c) 2015 Tucker Balch  		  	   		 	 	 		  		  		    	 		 		   		 		  
  		  	   		 	 	 		  		  		    	 		 		   		 		  
Copyright 2018, Georgia Institute of Technology (Georgia Tech)  		  	   		 	 	 		  		  		    	 		 		   		 		  
Atlanta, Georgia 30332  		  	   		 	 	 		  		  		    	 		 		   		 		  
All Rights Reserved  		  	   		 	 	 		  		  		    	 		 		   		 		  
  		  	   		 	 	 		  		  		    	 		 		   		 		  
Template code for CS 4646/7646  		  	   		 	 	 		  		  		    	 		 		   		 		  
  		  	   		 	 	 		  		  		    	 		 		   		 		  
Georgia Tech asserts copyright ownership of this template and all derivative  		  	   		 	 	 		  		  		    	 		 		   		 		  
works, including solutions to the projects assigned in this course. Students  		  	   		 	 	 		  		  		    	 		 		   		 		  
and other users of this template code are advised not to share it with others  		  	   		 	 	 		  		  		    	 		 		   		 		  
or to make it available on publicly viewable websites including repositories  		  	   		 	 	 		  		  		    	 		 		   		 		  
such as github and gitlab.  This copyright statement should not be removed  		  	   		 	 	 		  		  		    	 		 		   		 		  
or edited.  		  	   		 	 	 		  		  		    	 		 		   		 		  
  		  	   		 	 	 		  		  		    	 		 		   		 		  
We do grant permission to share solutions privately with non-students such  		  	   		 	 	 		  		  		    	 		 		   		 		  
as potential employers. However, sharing with other current or future  		  	   		 	 	 		  		  		    	 		 		   		 		  
students of CS 7646 is prohibited and subject to being investigated as a  		  	   		 	 	 		  		  		    	 		 		   		 		  
GT honor code violation.  		  	   		 	 	 		  		  		    	 		 		   		 		  
  		  	   		 	 	 		  		  		    	 		 		   		 		  
-----do not edit anything above this line---  		  	   		 	 	 		  		  		    	 		 		   		 		  
  		  	   		 	 	 		  		  		    	 		 		   		 		  
Student Name: Tucker Balch (replace with your name)  		  	   		 	 	 		  		  		    	 		 		   		 		  
GT User ID: omurphy8 (replace with your User ID)
GT ID: 904015662  		  	   		 	 	 		  		  		    	 		 		   		 		  
"""  		  	   		 	 	 		  		  		    	 		 		   		 		  
  		  	   		 	 	 		  		  		    	 		 		   		 		  
import random as rand  		  	   		 	 	 		  		  		    	 		 		   		 		  
  		  	   		 	 	 		  		  		    	 		 		   		 		  
import numpy as np

def author():  		  	   		 	 	 		  		  		    	 		 		   		 		  
    """  		  	   		 	 	 		  		  		    	 		 		   		 		  
    :return: The GT username of the student  		  	   		 	 	 		  		  		    	 		 		   		 		  
    :rtype: str  		  	   		 	 	 		  		  		    	 		 		   		 		  
    """  		  	   		 	 	 		  		  		    	 		 		   		 		  
    return "omurphy8"	  	 

def study_group():
    """
    Returns
        A comma separated string of GT_Name of each member of your study group
        # Example: "gburdell3, jdoe77, tbalch7" or "gburdell3" if a single individual working alone
    """
    return "omurphy8"
  		  	   		 	 	 		  		  		    	 		 		   		 		  
class QLearner(object):  		  	   		 	 	 		  		  		    	 		 		   		 		  
    """  		  	   		 	 	 		  		  		    	 		 		   		 		  
    This is a Q learner object.  		  	   		 	 	 		  		  		    	 		 		   		 		  
  		  	   		 	 	 		  		  		    	 		 		   		 		  
    :param num_states: The number of states to consider.  		  	   		 	 	 		  		  		    	 		 		   		 		  
    :type num_states: int  		  	   		 	 	 		  		  		    	 		 		   		 		  
    :param num_actions: The number of actions available..  		  	   		 	 	 		  		  		    	 		 		   		 		  
    :type num_actions: int  		  	   		 	 	 		  		  		    	 		 		   		 		  
    :param alpha: The learning rate used in the update rule. Should range between 0.0 and 1.0 with 0.2 as a typical value.  		  	   		 	 	 		  		  		    	 		 		   		 		  
    :type alpha: float  		  	   		 	 	 		  		  		    	 		 		   		 		  
    :param gamma: The discount rate used in the update rule. Should range between 0.0 and 1.0 with 0.9 as a typical value.  		  	   		 	 	 		  		  		    	 		 		   		 		  
    :type gamma: float  		  	   		 	 	 		  		  		    	 		 		   		 		  
    :param rar: Random action rate: the probability of selecting a random action at each step. Should range between 0.0 (no random actions) to 1.0 (always random action) with 0.5 as a typical value.  		  	   		 	 	 		  		  		    	 		 		   		 		  
    :type rar: float  		  	   		 	 	 		  		  		    	 		 		   		 		  
    :param radr: Random action decay rate, after each update, rar = rar * radr. Ranges between 0.0 (immediate decay to 0) and 1.0 (no decay). Typically 0.99.  		  	   		 	 	 		  		  		    	 		 		   		 		  
    :type radr: float  		  	   		 	 	 		  		  		    	 		 		   		 		  
    :param dyna: The number of dyna updates for each regular update. When Dyna is used, 200 is a typical value.  		  	   		 	 	 		  		  		    	 		 		   		 		  
    :type dyna: int  		  	   		 	 	 		  		  		    	 		 		   		 		  
    :param verbose: If “verbose” is True, your code can print out information for debugging.  		  	   		 	 	 		  		  		    	 		 		   		 		  
    :type verbose: bool  		  	   		 	 	 		  		  		    	 		 		   		 		  
    """  		  	   		 	 	 		  		  		    	 		 		   		 		  
    def __init__(  		  	   		 	 	 		  		  		    	 		 		   		 		  
        self,  		  	   		 	 	 		  		  		    	 		 		   		 		  
        num_states=100,  		  	   		 	 	 		  		  		    	 		 		   		 		  
        num_actions=4,  		  	   		 	 	 		  		  		    	 		 		   		 		  
        alpha=0.2,  		  	   		 	 	 		  		  		    	 		 		   		 		  
        gamma=0.9,  		  	   		 	 	 		  		  		    	 		 		   		 		  
        rar=0.5,  		  	   		 	 	 		  		  		    	 		 		   		 		  
        radr=0.99,  		  	   		 	 	 		  		  		    	 		 		   		 		  
        dyna=0,  		  	   		 	 	 		  		  		    	 		 		   		 		  
        verbose=False,  		  	   		 	 	 		  		  		    	 		 		   		 		  
    ):  		  	   		 	 	 		  		  		    	 		 		   		 		  
        """  		  	   		 	 	 		  		  		    	 		 		   		 		  
        Constructor method  		  	   		 	 	 		  		  		    	 		 		   		 		  
        """  		  	   		 	 	 		  		  		    	 		 		   		 		  
        self.verbose = verbose                                                                                                
        self.num_states = num_states
        self.num_actions = num_actions                                                                                                
        self.alpha = alpha
        self.gamma = gamma
        self.rar = rar
        self.radr = radr
        self.dyna = dyna
        self.s = 0                                                                                                
        self.a = 0  		

        # 初始化 Q 表格
        self.Q = np.zeros((num_states, num_actions))  	

        # Dyna-Q 模型初始化
        if self.dyna > 0:   
            # 存储 S, A 元组的列表，用于随机选择幻觉经验
            self.experience = set()
            # 转换模型 T[s, a] -> s_prime。使用一个列表来存储所有观察到的 s_prime
            # 因为转换在导航问题中可能是随机的。
            # 但是，对于确定性或近乎确定性的转换，我们可以只存储最近的 s_prime
            self.T_model = {} # T_model[s][a] = [s_prime_1, s_prime_2, ...]
            # 奖励模型 R[s, a] -> r。使用一个字典存储 (s, a) 对应的最近奖励
            self.R_model = np.zeros((num_states, num_actions)) 

    def author(test="test"):  		  	   		 	 	 		  		  		    	 		 		   		 		  
        """  		  	   		 	 	 		  		  		    	 		 		   		 		  
        :return: The GT username of the student  		  	   		 	 	 		  		  		    	 		 		   		 		  
        :rtype: str  		  	   		 	 	 		  		  		    	 		 		   		 		  
        """  		  	
        print("find me:", test)   		 	 	 		  		  		    	 		 		   		 		  
        return "omurphy8"

    def study_group():
        """
        Returns
            A comma separated string of GT_Name of each member of your study group
            # Example: "gburdell3, jdoe77, tbalch7" or "gburdell3" if a single individual working alone
        """
        return "omurphy8"	      
    
    def _choose_action(self, s):
        """
        根据 rar 和 Q 表格选择动作 (epsilon-贪婪)
        """
        if rand.random() < self.rar:
            # 随机动作
            action = rand.randint(0, self.num_actions - 1)
        else:
            # 贪婪动作: 选择 Q[s, :] 中最大的动作
            # 使用 argmax 以解决多个最大值的情况
            q_values = self.Q[s, :]
            best_actions = np.where(q_values == np.max(q_values))[0]
            action = rand.choice(best_actions)
        return action   	 		  		  		    	 		 		   		 		  
  		  	   		 	 	 		  		  		    	 		 		   		 		  
    def querysetstate(self, s):  		  	   		 	 	 		  		  		    	 		 		   		 		  
        """  		  	   		 	 	 		  		  		    	 		 		   		 		  
        Update the state without updating the Q-table  		  	   		 	 	 		  		  		    	 		 		   		 		  
  		  	   		 	 	 		  		  		    	 		 		   		 		  
        :param s: The new state  		  	   		 	 	 		  		  		    	 		 		   		 		  
        :type s: int  		  	   		 	 	 		  		  		    	 		 		   		 		  
        :return: The selected action  		  	   		 	 	 		  		  		    	 		 		   		 		  
        :rtype: int  		  	   		 	 	 		  		  		    	 		 		   		 		  
        """  		  	   		 	 	 		  		  		    	 		 		   		 		  
        self.s = s  		  	   		 	 	 		  		  		    	 		 		   		 		  
        action = self._choose_action(s)	
        self.a = action	  	   		 	
        if self.verbose:                                                                                              
            print(f"s = {s}, a = {action}")                                                                                               
        return action 	 		  		  		    	 		 		   		 		  
  		  	   		 	 	 		  		  		    	 		 		   		 		  
    def query(self, s_prime, r):  		  	   		 	 	 		  		  		    	 		 		   		 		  
        """  		  	   		 	 	 		  		  		    	 		 		   		 		  
        Update the Q table and return an action  		  	   		 	 	 		  		  		    	 		 		   		 		  
  		  	   		 	 	 		  		  		    	 		 		   		 		  
        :param s_prime: The new state  		  	   		 	 	 		  		  		    	 		 		   		 		  
        :type s_prime: int  		  	   		 	 	 		  		  		    	 		 		   		 		  
        :param r: The immediate reward  		  	   		 	 	 		  		  		    	 		 		   		 		  
        :type r: float  		  	   		 	 	 		  		  		    	 		 		   		 		  
        :return: The selected action  		  	   		 	 	 		  		  		    	 		 		   		 		  
        :rtype: int  		  	   		 	 	 		  		  		    	 		 		   		 		  
        """  		  	   		 

        s = self.s
        a = self.a

        # 1. Q-Table 更新 (真实经验)
        # Q[s, a] <- (1 - alpha) * Q[s, a] + alpha * (r + gamma * max_a' Q[s_prime, a'])
        max_q_prime = np.max(self.Q[s_prime, :])
        self.Q[s, a] = (1 - self.alpha) * self.Q[s, a] + self.alpha * (r + self.gamma * max_q_prime)
        
        # 2. Dyna-Q (模型学习和幻觉更新)
        if self.dyna > 0:
            # 2a. 模型学习 (存储经验: s, a, s_prime, r)
            self.experience.add((s, a))
            self.R_model[s, a] = r # 存储最近的奖励
            
            # 存储转换模型
            if s not in self.T_model:
                self.T_model[s] = {}
            if a not in self.T_model[s]:
                self.T_model[s][a] = []
                
            # 清除旧的，只存储最新的 s_prime，因为 T 可能是确定性的
            # 也可以存储计数并从中采样，但只存储最新的 s' 通常可以简化模型
            self.T_model[s][a] = s_prime

            # 2b. 幻觉更新
            experience_list = list(self.experience)
            for _ in range(self.dyna):
                # 随机选择一个以前经历过的状态-动作对 (s_rand, a_rand)
                s_rand, a_rand = rand.choice(experience_list)
                
                # 从模型中获取预测的 s'_rand 和 r_rand
                r_rand = self.R_model[s_rand, a_rand]
                
                # 获取 s'_rand
                if a_rand in self.T_model[s_rand]:
                    s_prime_rand = self.T_model[s_rand][a_rand]
                else:
                    # 如果 s_rand, a_rand 存在于 self.experience，则它们也应该存在于 self.T_model/R_model，
                    # 除非 self.T_model 的结构更复杂。
                    # 为了安全，如果找不到，就跳过这个幻觉步骤（但这不应该发生）
                    continue 
                
                # 使用幻觉经验更新 Q 表格
                max_q_prime_rand = np.max(self.Q[s_prime_rand, :])
                self.Q[s_rand, a_rand] = (1 - self.alpha) * self.Q[s_rand, a_rand] + self.alpha * (r_rand + self.gamma * max_q_prime_rand)

        # 3. 选择下一个动作 a' (基于 s_prime)
        action = self._choose_action(s_prime)
        
        # 4. 衰减 rar
        self.rar *= self.radr

        # 5. 更新 s 和 a
        self.s = s_prime                                                                                                
        self.a = action
        
        if self.verbose:                                                                                              
            print(f"s = {s_prime}, a = {action}, r={r}, rar={self.rar}")                                                                                              
        return action

  		  	   		 	 	 		  		  		    	 		 		   		 		  
if __name__ == "__main__":  		  	   		 	 	 		  		  		    	 		 		   		 		  
    print("Remember Q from Star Trek? Well, this isn't him")  		
