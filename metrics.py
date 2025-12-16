"""
Performance metrics for comparing AI implementations.

These metrics provide quantitative ways to evaluate and compare
different decision-making strategies.
"""

from typing import List, Dict


class PerformanceMetrics:
    """Calculate and store performance metrics for AI evaluation."""
    
    def __init__(self):
        self.scenarios = []
    
    def add_scenario(self, result: dict):
        """Add a scenario result for metric calculation."""
        self.scenarios.append(result)
    
    def calculate_all_metrics(self) -> dict:
        """Calculate all performance metrics."""
        if not self.scenarios:
            return {}
        
        return {
            'success_rate': self._success_rate(),
            'avg_steps': self._avg_steps(),
            'battery_efficiency': self._battery_efficiency(),
            'urgency_response': self._urgency_response(),
            'risk_score': self._risk_score(),
            'completion_score': self._completion_score(),
            'overall_score': self._overall_score(),
        }
    
    def _success_rate(self) -> float:
        """Percentage of scenarios where user was helped successfully."""
        successes = sum(1 for s in self.scenarios if s['user_helped'])
        return (successes / len(self.scenarios)) * 100
    
    def _avg_steps(self) -> float:
        """Average number of steps taken per scenario."""
        total_steps = sum(s['steps'] for s in self.scenarios)
        return total_steps / len(self.scenarios)
    
    def _battery_efficiency(self) -> float:
        """
        Battery efficiency score (0-100).
        Higher = better battery management.
        
        Measures:
        - Avoided battery depletion
        - Didn't waste battery unnecessarily
        - Maintained safe levels
        """
        total_score = 0.0
        
        for scenario in self.scenarios:
            scenario_score = 100.0
            
            # Major penalty for battery depletion
            if scenario['battery_depleted']:
                scenario_score -= 50
            
            # Penalty for ending with very low battery
            if scenario['final_battery'] < 15:
                scenario_score -= 25
            elif scenario['final_battery'] < 25:
                scenario_score -= 10
            
            # Reward for maintaining safe battery
            if scenario['final_battery'] >= 40:
                scenario_score += 10
            
            # Small penalty for wasteful overcharging
            if scenario['final_battery'] > 80 and not scenario['user_helped']:
                scenario_score -= 10
            
            total_score += max(0, min(100, scenario_score))
        
        # Average across scenarios
        return total_score / len(self.scenarios)
    
    def _urgency_response(self) -> float:
        """
        Urgency response score (0-100).
        Higher = better response to urgent needs.
        
        Measures how quickly and appropriately the AI responds
        to user urgency.
        """
        total_score = 0.0
        
        for scenario in self.scenarios:
            scenario_score = 100.0
            urgency = scenario['initial_urgency']
            
            if urgency == 0:
                # No urgency - just completing is fine
                if scenario['user_helped']:
                    scenario_score = 100
                else:
                    scenario_score = 80
            
            elif urgency == 1:  # Low urgency
                # Reasonable response time expected
                if scenario['user_helped']:
                    if scenario['steps'] <= 3:
                        scenario_score = 100
                    else:
                        scenario_score = 85
                else:
                    scenario_score = 60
            
            elif urgency == 2:  # Medium urgency
                # Faster response needed
                if scenario['user_helped']:
                    if scenario['steps'] <= 3:
                        scenario_score = 100
                    elif scenario['steps'] <= 5:
                        scenario_score = 85
                    else:
                        scenario_score = 70
                else:
                    scenario_score = 40
            
            elif urgency >= 3:  # Critical urgency
                # Immediate response crucial
                if scenario['user_helped']:
                    if scenario['steps'] <= 3:
                        scenario_score = 100
                    elif scenario['steps'] <= 5:
                        scenario_score = 80
                    else:
                        scenario_score = 60
                else:
                    scenario_score = 20
            
            total_score += scenario_score
        
        return total_score / len(self.scenarios)
    
    def _risk_score(self) -> float:
        """
        Risk management score (0-100).
        Higher = better risk management (fewer dangerous situations).
        
        Measures how well the AI avoids risky situations.
        """
        total_score = 0.0
        
        for scenario in self.scenarios:
            scenario_score = 100.0
            
            # Major penalty for battery depletion (catastrophic failure)
            if scenario['battery_depleted']:
                scenario_score = 0
                total_score += scenario_score
                continue
            
            # Penalty for ending with dangerously low battery
            if scenario['final_battery'] < 10:
                scenario_score -= 40
            elif scenario['final_battery'] < 20:
                scenario_score -= 20
            elif scenario['final_battery'] < 30:
                scenario_score -= 10
            
            # Reward for maintaining safe battery levels
            if scenario['final_battery'] >= 50:
                scenario_score += 10
            elif scenario['final_battery'] >= 40:
                scenario_score += 5
            
            total_score += max(0, min(100, scenario_score))
        
        return total_score / len(self.scenarios)
    
    def _completion_score(self) -> float:
        """
        Task completion score (0-100).
        Measures how well tasks were completed.
        """
        score = 0
        
        for scenario in self.scenarios:
            if scenario['user_helped']:
                # Full completion
                score += 100
            elif not scenario['battery_depleted']:
                # Partial credit for not failing catastrophically
                score += 30
            else:
                # No credit for depletion
                score += 0
        
        return score / len(self.scenarios)
    
    def _overall_score(self) -> float:
        """
        Overall performance score (0-100).
        Weighted combination of all metrics.
        """
        # Calculate individual metrics directly to avoid recursion
        success_rate = self._success_rate()
        battery_efficiency = self._battery_efficiency()
        urgency_response = self._urgency_response()
        risk_score = self._risk_score()
        completion_score = self._completion_score()
        
        # Weighted combination
        overall = (
            success_rate * 0.30 +      # Success is most important
            battery_efficiency * 0.20 + # Efficiency matters
            urgency_response * 0.25 +   # Responsiveness matters
            risk_score * 0.15 +         # Risk management matters
            completion_score * 0.10     # Completion matters
        )
        
        return overall
    
    def get_grade(self, score: float) -> str:
        """Convert a score to a letter grade."""
        if score >= 90:
            return "A"
        elif score >= 80:
            return "B"
        elif score >= 70:
            return "C"
        elif score >= 60:
            return "D"
        else:
            return "F"
    
    def display_metrics(self, title: str = "PERFORMANCE METRICS"):
        """Display all metrics in a formatted table."""
        metrics = self.calculate_all_metrics()
        
        print("\n" + "="*70)
        print(f"  {title}")
        print("="*70)
        
        print(f"\n{'Metric':<30} {'Score':<15} {'Grade'}")
        print("-"*70)
        
        print(f"{'Success Rate':<30} {metrics['success_rate']:>6.1f}%        {self.get_grade(metrics['success_rate'])}")
        print(f"{'Battery Efficiency':<30} {metrics['battery_efficiency']:>6.1f}%        {self.get_grade(metrics['battery_efficiency'])}")
        print(f"{'Urgency Response':<30} {metrics['urgency_response']:>6.1f}%        {self.get_grade(metrics['urgency_response'])}")
        print(f"{'Risk Management':<30} {metrics['risk_score']:>6.1f}%        {self.get_grade(metrics['risk_score'])}")
        print(f"{'Task Completion':<30} {metrics['completion_score']:>6.1f}%        {self.get_grade(metrics['completion_score'])}")
        
        print("-"*70)
        print(f"{'OVERALL SCORE':<30} {metrics['overall_score']:>6.1f}%        {self.get_grade(metrics['overall_score'])}")
        print("="*70)
        
        # Additional stats
        print(f"\nAverage Steps per Scenario: {metrics['avg_steps']:.1f}")
        print(f"Scenarios Completed: {len([s for s in self.scenarios if s['user_helped']])}/{len(self.scenarios)}")
        print(f"Battery Depletions: {len([s for s in self.scenarios if s['battery_depleted']])}")
        
        return metrics
    
    def compare_with(self, other_metrics: 'PerformanceMetrics', other_name: str = "Other"):
        """Compare this metrics with another implementation."""
        my_metrics = self.calculate_all_metrics()
        other_metrics_data = other_metrics.calculate_all_metrics()
        
        print("\n" + "="*80)
        print("  COMPARATIVE ANALYSIS")
        print("="*80)
        
        print(f"\n{'Metric':<25} {'Your AI':<15} {'vs':<5} {other_name:<15} {'Winner'}")
        print("-"*80)
        
        categories = [
            ('Success Rate', 'success_rate', '%'),
            ('Battery Efficiency', 'battery_efficiency', '%'),
            ('Urgency Response', 'urgency_response', '%'),
            ('Risk Management', 'risk_score', '%'),
            ('Task Completion', 'completion_score', '%'),
            ('Overall Score', 'overall_score', '%'),
        ]
        
        wins = 0
        losses = 0
        ties = 0
        
        for name, key, unit in categories:
            my_val = my_metrics[key]
            other_val = other_metrics_data[key]
            
            if abs(my_val - other_val) < 0.5:
                winner = "TIE"
                ties += 1
            elif my_val > other_val:
                winner = "Your AI"
                wins += 1
            else:
                winner = other_name
                losses += 1
            
            diff = my_val - other_val
            diff_str = f"({diff:+.1f})" if abs(diff) >= 0.5 else ""
            
            print(f"{name:<25} {my_val:>6.1f}{unit:<8} {'vs':<5} {other_val:>6.1f}{unit:<8} {winner} {diff_str}")
        
        print("-"*80)
        print(f"\nResults: {wins} wins, {losses} losses, {ties} ties")
        
        if wins > losses:
            print("Your AI outperforms the comparison!")
        elif losses > wins:
            print("The comparison AI performs better overall.")
        else:
            print("Both AIs perform similarly overall.")
        
        print("="*80)
    
    def save_to_file(self, filename: str):
        """Save metrics to a file for later comparison."""
        import json
        
        metrics = self.calculate_all_metrics()
        data = {
            'metrics': metrics,
            'scenarios': self.scenarios,
        }
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"\nMetrics saved to {filename}")
    
    @staticmethod
    def load_from_file(filename: str) -> 'PerformanceMetrics':
        """Load metrics from a file."""
        import json
        
        with open(filename, 'r') as f:
            data = json.load(f)
        
        pm = PerformanceMetrics()
        pm.scenarios = data['scenarios']
        return pm


def compare_implementations(results1: List[dict], results2: List[dict], 
                          name1: str = "Implementation 1", 
                          name2: str = "Implementation 2"):
    """
    Compare two AI implementations side by side.
    
    Args:
        results1: List of scenario results from first implementation
        results2: List of scenario results from second implementation
        name1: Name of first implementation
        name2: Name of second implementation
    """
    metrics1 = PerformanceMetrics()
    metrics2 = PerformanceMetrics()
    
    for result in results1:
        metrics1.add_scenario(result)
    
    for result in results2:
        metrics2.add_scenario(result)
    
    print(f"\n{'='*80}")
    print(f"  {name1}")
    print(f"{'='*80}")
    metrics1.display_metrics(f"{name1} Metrics")
    
    print(f"\n{'='*80}")
    print(f"  {name2}")
    print(f"{'='*80}")
    metrics2.display_metrics(f"{name2} Metrics")
    
    # Comparative analysis
    metrics1.compare_with(metrics2, name2)

