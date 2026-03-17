"""
Student Model - Advanced knowledge tracking.
Implements a simplified Bayesian Knowledge Tracing (BKT) approach 
to estimate the probability that a student has mastered a phoneme.
"""

def update_mastery_probability(
    current_p: float, 
    correct: bool,
    p_transit: float = 0.1,  # Probability of learning between attempts
    p_slip: float = 0.1,     # Probability of making a mistake despite knowing
    p_guess: float = 0.2     # Probability of guessing correctly without knowing
) -> float:
    """
    Standard BKT Update Rule.
    
    current_p: prior probability of mastery.
    correct: whether the last attempt was correct.
    """
    
    if correct:
        # Probability of knowing, given they got it right
        p_known_given_obs = (current_p * (1 - p_slip)) / (current_p * (1 - p_slip) + (1 - current_p) * p_guess)
    else:
        # Probability of knowing, given they got it wrong
        p_known_given_obs = (current_p * p_slip) / (current_p * p_slip + (1 - current_p) * (1 - p_guess))
        
    # Account for transition (learning)
    new_p_mastery = p_known_given_obs + (1 - p_known_given_obs) * p_transit
    
    return min(0.99, max(0.01, new_p_mastery))

def get_recommendation(mastery_p: float) -> str:
    """Returns pedagogical action based on mastery probability."""
    if mastery_p > 0.85:
        return "ADVANCE"
    elif mastery_p > 0.50:
        return "REINFORCE"
    else:
        return "RETEACH"
