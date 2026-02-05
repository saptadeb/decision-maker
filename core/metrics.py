"""
Performance metrics for comparing AI implementations.

This module provides a comprehensive metrics system for quantitatively evaluating
and comparing different decision-making strategies. Metrics cover multiple dimensions
including success rate, battery efficiency, urgency response, risk management, and
overall task completion.

The metrics system enables:
- Objective comparison between different AI implementations
- Identification of strengths and weaknesses in decision strategies
- Tracking of improvement over multiple iterations
- Grade-based assessment of performance

See docs/METRICS.md for detailed documentation of each metric.
"""

from typing import List, Dict


class PerformanceMetrics:
    """
    Calculate and store performance metrics for AI evaluation.
    
    This class accumulates results from multiple scenario runs and calculates
    comprehensive performance metrics across six dimensions:
    1. Success Rate - percentage of scenarios where user was helped
    2. Battery Efficiency - how well battery resources were managed
    3. Urgency Response - how quickly urgent situations were addressed
    4. Risk Management - how well dangerous situations were avoided
    5. Task Completion - overall task completion quality
    6. Overall Score - weighted combination of all metrics
    
    Usage:
        metrics = PerformanceMetrics()
        for result in scenario_results:
            metrics.add_scenario(result)
        metrics.display_metrics()
    """
    
    def __init__(self):
        self.scenarios = []
    
    def add_scenario(self, result: dict):
        """
        Add a scenario result for metric calculation.
        
        Args:
            result: Dictionary containing scenario results with keys:
                   - name: Scenario name
                   - initial_battery: Starting battery level
                   - initial_urgency: Starting urgency level
                   - steps: Number of steps taken
                   - final_battery: Ending battery level
                   - user_helped: Boolean, whether user urgency reached 0
                   - battery_depleted: Boolean, whether battery reached 0
        """
        self.scenarios.append(result)
    
    def calculate_all_metrics(self) -> dict:
        """
        Calculate all performance metrics.
        
        Returns:
            dict: Dictionary containing all calculated metrics:
                 - success_rate: 0-100%
                 - avg_steps: Average steps per scenario
                 - battery_efficiency: 0-100%
                 - urgency_response: 0-100%
                 - risk_score: 0-100%
                 - completion_score: 0-100%
                 - overall_score: 0-100% (weighted combination)
                 
        Returns empty dict if no scenarios have been added.
        """
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
        """
        Calculate success rate metric.
        
        Returns:
            float: Percentage (0-100) of scenarios where user was successfully
                  helped (urgency reduced to 0)
        """
        successes = sum(1 for s in self.scenarios if s['user_helped'])
        return (successes / len(self.scenarios)) * 100
    
    def _avg_steps(self) -> float:
        """
        Calculate average steps per scenario.
        
        Returns:
            float: Mean number of steps taken across all scenarios
        """
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
        """
        Convert a numerical score to a letter grade.
        
        Args:
            score: Numerical score (0-100)
            
        Returns:
            str: Letter grade (A, B, C, D, or F)
                A: 90-100
                B: 80-89
                C: 70-79
                D: 60-69
                F: <60
        """
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
        """
        Display all metrics in a formatted table.
        
        Prints a comprehensive report including:
        - Individual metric scores with letter grades
        - Overall score
        - Additional statistics (avg steps, completions, depletions)
        
        Args:
            title: Header title for the metrics display
            
        Returns:
            dict: The calculated metrics dictionary (for further use)
        """
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
        """
        Compare this metrics with another implementation.
        
        Displays a side-by-side comparison showing which implementation
        performs better in each category.
        
        Args:
            other_metrics: Another PerformanceMetrics object to compare against
            other_name: Display name for the other implementation
        """
        my_metrics = self.calculate_all_metrics()
        other_metrics_data = other_metrics.calculate_all_metrics()
        
        print("\n" + "="*80)
        print("  COMPARATIVE ANALYSIS")
        print("="*80)
        
        print(f"\n{'Metric':<25} {'Custom AI':<15} {'vs':<5} {other_name:<15} {'Winner'}")
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
                winner = "Custom AI"
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
            print("Custom AI outperforms the comparison!")
        elif losses > wins:
            print("The comparison AI performs better overall.")
        else:
            print("Both AIs perform similarly overall.")
        
        print("="*80)
    
    def save_to_file(self, filename: str):
        """
        Save metrics to a JSON file for later comparison.
        
        Args:
            filename: Path to save the metrics JSON file
                     (typically in output/ directory)
        """
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
        """
        Load metrics from a previously saved JSON file.
        
        Args:
            filename: Path to the metrics JSON file
            
        Returns:
            PerformanceMetrics: Reconstructed metrics object with
                               scenarios loaded from file
        """
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
    
    Creates PerformanceMetrics objects for both implementations and
    displays their metrics along with a comparative analysis.
    
    Args:
        results1: List of scenario results from first implementation
                 (each result should be a dict with required keys)
        results2: List of scenario results from second implementation
        name1: Display name for first implementation
        name2: Display name for second implementation
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

