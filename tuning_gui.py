"""
Parameter Tuning GUI

This GUI allows users to tune implementation parameters without coding.
They can adjust thresholds, weights, and strategies using sliders and see
results in real-time.
"""

import tkinter as tk
from tkinter import ttk, scrolledtext
from dataclasses import replace

from core.state import RobotState
from core.actions import Action
from core.simulator import RobotSimulator
from core.constraints import is_action_allowed
from config.loader import load_params


class TuningGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Parameter Tuning GUI")
        self.root.geometry("1000x700")
        
        # Load defaults from config
        default_values = load_params()
        
        # Tunable parameters
        self.params = {
            'recharge_threshold': tk.IntVar(value=default_values['recharge_threshold']),
            'critical_battery': tk.IntVar(value=default_values['critical_battery']),
            'help_min_battery': tk.IntVar(value=default_values['help_min_battery']),
            'safety_weight': tk.DoubleVar(value=default_values['safety_weight']),
            'helpfulness_weight': tk.DoubleVar(value=default_values['helpfulness_weight']),
            'proactive_recharge': tk.BooleanVar(value=default_values['proactive_recharge']),
            'risk_tolerance': tk.StringVar(value=default_values['risk_tolerance']),
        }
        
        self.create_layout()
        
    def create_layout(self):
        """Create the GUI layout."""
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Left: Parameters
        self.create_params_panel(main_frame)
        
        # Right: Testing
        self.create_test_panel(main_frame)
        
    def create_params_panel(self, parent):
        """Create parameter tuning panel."""
        params_frame = ttk.LabelFrame(parent, text="Tune AI Parameters", padding="15")
        params_frame.grid(row=0, column=0, rowspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 5))
        
        row = 0
        
        # Header
        ttk.Label(params_frame, text="Adjust these parameters to change AI behavior:", 
                 font=('TkDefaultFont', 9, 'bold')).grid(row=row, column=0, columnspan=3, sticky=tk.W, pady=(0, 15))
        row += 1
        
        # Battery Management Section
        ttk.Label(params_frame, text="Battery Management", 
                 font=('TkDefaultFont', 9, 'bold')).grid(row=row, column=0, columnspan=3, sticky=tk.W, pady=(10, 5))
        row += 1
        
        # Recharge Threshold
        ttk.Label(params_frame, text="Recharge When Battery Below:").grid(row=row, column=0, sticky=tk.W, pady=5)
        ttk.Scale(params_frame, from_=10, to=70, variable=self.params['recharge_threshold'],
                 orient=tk.HORIZONTAL, length=150).grid(row=row, column=1, sticky=(tk.W, tk.E), pady=5)
        self.recharge_label = ttk.Label(params_frame, text="30%")
        self.recharge_label.grid(row=row, column=2, padx=5)
        self.params['recharge_threshold'].trace('w', self.update_recharge_label)
        row += 1
        
        # Critical Battery
        ttk.Label(params_frame, text="Critical Battery Level:").grid(row=row, column=0, sticky=tk.W, pady=5)
        ttk.Scale(params_frame, from_=5, to=25, variable=self.params['critical_battery'],
                 orient=tk.HORIZONTAL, length=150).grid(row=row, column=1, sticky=(tk.W, tk.E), pady=5)
        self.critical_label = ttk.Label(params_frame, text="15%")
        self.critical_label.grid(row=row, column=2, padx=5)
        self.params['critical_battery'].trace('w', self.update_critical_label)
        row += 1
        
        # Min Battery for Helping
        ttk.Label(params_frame, text="Min Battery to Help:").grid(row=row, column=0, sticky=tk.W, pady=5)
        ttk.Scale(params_frame, from_=10, to=40, variable=self.params['help_min_battery'],
                 orient=tk.HORIZONTAL, length=150).grid(row=row, column=1, sticky=(tk.W, tk.E), pady=5)
        self.help_min_label = ttk.Label(params_frame, text="20%")
        self.help_min_label.grid(row=row, column=2, padx=5)
        self.params['help_min_battery'].trace('w', self.update_help_min_label)
        row += 1
        
        # Proactive Recharge
        ttk.Checkbutton(params_frame, text="Enable Proactive Recharging", 
                       variable=self.params['proactive_recharge']).grid(row=row, column=0, columnspan=3, sticky=tk.W, pady=5)
        row += 1
        
        # Priority Weights Section
        ttk.Separator(params_frame, orient=tk.HORIZONTAL).grid(row=row, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=15)
        row += 1
        
        ttk.Label(params_frame, text="Priority Weights", 
                 font=('TkDefaultFont', 9, 'bold')).grid(row=row, column=0, columnspan=3, sticky=tk.W, pady=(0, 5))
        row += 1
        
        # Safety Weight
        ttk.Label(params_frame, text="Safety Priority:").grid(row=row, column=0, sticky=tk.W, pady=5)
        ttk.Scale(params_frame, from_=0.0, to=1.0, variable=self.params['safety_weight'],
                 orient=tk.HORIZONTAL, length=150).grid(row=row, column=1, sticky=(tk.W, tk.E), pady=5)
        self.safety_label = ttk.Label(params_frame, text="0.40")
        self.safety_label.grid(row=row, column=2, padx=5)
        self.params['safety_weight'].trace('w', self.update_safety_label)
        row += 1
        
        # Helpfulness Weight
        ttk.Label(params_frame, text="Helpfulness Priority:").grid(row=row, column=0, sticky=tk.W, pady=5)
        ttk.Scale(params_frame, from_=0.0, to=1.0, variable=self.params['helpfulness_weight'],
                 orient=tk.HORIZONTAL, length=150).grid(row=row, column=1, sticky=(tk.W, tk.E), pady=5)
        self.helpfulness_label = ttk.Label(params_frame, text="0.60")
        self.helpfulness_label.grid(row=row, column=2, padx=5)
        self.params['helpfulness_weight'].trace('w', self.update_helpfulness_label)
        row += 1
        
        # Strategy Section
        ttk.Separator(params_frame, orient=tk.HORIZONTAL).grid(row=row, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=15)
        row += 1
        
        ttk.Label(params_frame, text="Risk Strategy", 
                 font=('TkDefaultFont', 9, 'bold')).grid(row=row, column=0, columnspan=3, sticky=tk.W, pady=(0, 5))
        row += 1
        
        risk_options = ["Conservative", "Medium", "Aggressive"]
        ttk.Label(params_frame, text="Risk Tolerance:").grid(row=row, column=0, sticky=tk.W, pady=5)
        ttk.Combobox(params_frame, textvariable=self.params['risk_tolerance'], 
                    values=risk_options, state="readonly", width=15).grid(row=row, column=1, columnspan=2, sticky=tk.W, pady=5)
        row += 1
        
        # Buttons
        ttk.Separator(params_frame, orient=tk.HORIZONTAL).grid(row=row, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=15)
        row += 1
        
        btn_frame = ttk.Frame(params_frame)
        btn_frame.grid(row=row, column=0, columnspan=3, pady=5)
        
        ttk.Button(btn_frame, text="Test Current Settings", command=self.test_settings,
                  style='Accent.TButton').pack(fill=tk.X, pady=2)
        ttk.Button(btn_frame, text="Reset to Defaults", command=self.reset_defaults).pack(fill=tk.X, pady=2)
        ttk.Button(btn_frame, text="Export to Code", command=self.export_code).pack(fill=tk.X, pady=2)
        
    def create_test_panel(self, parent):
        """Create testing panel."""
        test_frame = ttk.LabelFrame(parent, text="Test Results", padding="10")
        test_frame.grid(row=0, column=1, rowspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        test_frame.columnconfigure(0, weight=1)
        test_frame.rowconfigure(0, weight=1)
        
        # Output area
        self.output_text = scrolledtext.ScrolledText(test_frame, wrap=tk.WORD, 
                                                     width=60, height=35, 
                                                     font=('Courier', 9))
        self.output_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure tags
        self.output_text.tag_config("header", foreground="#0066cc", font=('Courier', 9, 'bold'))
        self.output_text.tag_config("success", foreground="#009900")
        self.output_text.tag_config("failure", foreground="#cc0000")
        self.output_text.tag_config("info", foreground="#666666")
        
        self.log("Adjust parameters on the left and click 'Test Current Settings' to see results.\n\n", "info")
    
    # Label update callbacks
    def update_recharge_label(self, *args):
        self.recharge_label.config(text=f"{self.params['recharge_threshold'].get()}%")
    
    def update_critical_label(self, *args):
        self.critical_label.config(text=f"{self.params['critical_battery'].get()}%")
    
    def update_help_min_label(self, *args):
        self.help_min_label.config(text=f"{self.params['help_min_battery'].get()}%")
    
    def update_safety_label(self, *args):
        self.safety_label.config(text=f"{self.params['safety_weight'].get():.2f}")
    
    def update_helpfulness_label(self, *args):
        self.helpfulness_label.config(text=f"{self.params['helpfulness_weight'].get():.2f}")
    
    def tuned_decision(self, state: RobotState) -> Action:
        """Decision logic using tuned parameters."""
        params = {k: v.get() for k, v in self.params.items()}
        
        # Strategy based on risk tolerance
        if params['risk_tolerance'] == "Conservative":
            battery_buffer = 1.5
        elif params['risk_tolerance'] == "Aggressive":
            battery_buffer = 0.7
        else:
            battery_buffer = 1.0
        
        # Critical battery - must recharge
        if state.battery < params['critical_battery']:
            if state.user_urgency >= 3 and state.battery >= 10:
                return Action.HELP_USER
            elif state.battery >= 10:
                return Action.RECHARGE
            else:
                return Action.CALL_FOR_HELP
        
        # High urgency - help if possible
        if state.user_urgency >= 2 and state.battery >= params['help_min_battery']:
            return Action.HELP_USER
        
        # Low battery - recharge
        if state.battery < params['recharge_threshold'] * battery_buffer:
            if params['proactive_recharge'] or state.user_urgency == 0:
                return Action.RECHARGE
        
        # Any urgency with decent battery - help
        if state.user_urgency >= 1 and state.battery >= params['help_min_battery']:
            return Action.HELP_USER
        
        # No urgency - recharge if needed
        if state.battery < params['recharge_threshold']:
            return Action.RECHARGE
        
        # Default - wait
        return Action.WAIT
    
    def test_settings(self):
        """Test current settings on sample scenarios."""
        self.output_text.delete(1.0, tk.END)
        self.log("Testing with Current Parameters\n", "header")
        self.log("=" * 60 + "\n\n", "header")
        
        # Test scenarios - all 12 scenarios from gui.py
        scenarios = [
            ("Balanced Start", RobotState(battery=50, user_urgency=1, distance_to_user=5.0, 
                                         distance_to_charger=10.0), 8),
            ("Low Battery Crisis", RobotState(battery=25, user_urgency=2, distance_to_user=3.0,
                                             distance_to_charger=15.0, time_pressure=True), 6),
            ("Critical Battery", RobotState(battery=15, user_urgency=1, distance_to_user=8.0,
                                           distance_to_charger=5.0), 8),
            ("Urgent User - Good Battery", RobotState(battery=80, user_urgency=3, distance_to_user=2.0,
                                                      distance_to_charger=20.0, time_pressure=True), 6),
            ("Empty Battery Recovery", RobotState(battery=5, user_urgency=0, distance_to_user=10.0,
                                                  distance_to_charger=3.0), 6),
            ("High Urgency - Far Charger", RobotState(battery=40, user_urgency=3, distance_to_user=2.0,
                                                      distance_to_charger=25.0, time_pressure=True), 8),
            ("Multiple Needs", RobotState(battery=60, user_urgency=2, distance_to_user=8.0,
                                         distance_to_charger=8.0, time_pressure=True), 10),
            ("Efficiency Test", RobotState(battery=100, user_urgency=1, distance_to_user=15.0,
                                          distance_to_charger=15.0), 12),
            ("Close to Charger", RobotState(battery=20, user_urgency=2, distance_to_user=10.0,
                                           distance_to_charger=2.0, time_pressure=True), 8),
            ("Close to User", RobotState(battery=30, user_urgency=3, distance_to_user=1.0,
                                        distance_to_charger=20.0, time_pressure=True), 6),
            ("Moderate Everything", RobotState(battery=50, user_urgency=2, distance_to_user=10.0,
                                              distance_to_charger=10.0, time_pressure=True), 10),
            ("Low Urgency - Low Battery", RobotState(battery=20, user_urgency=1, distance_to_user=5.0,
                                                     distance_to_charger=8.0), 8),
        ]
        
        successes = 0
        for name, state, max_steps in scenarios:
            result = self.run_scenario(name, state, max_steps)
            if result['success']:
                successes += 1
        
        self.log(f"\n{'=' * 60}\n", "header")
        self.log(f"Results: {successes}/{len(scenarios)} scenarios completed successfully\n", 
                "success" if successes == len(scenarios) else "failure")
    
    def run_scenario(self, name, initial_state, max_steps):
        """Run a scenario with tuned parameters."""
        self.log(f"\n{name}:\n", "header")
        self.log(f"Initial: Battery={initial_state.battery}%, Urgency={initial_state.user_urgency}\n", "info")
        
        state_copy = replace(initial_state)
        sim = RobotSimulator(state_copy, max_steps)
        
        step = 0
        while not sim.scenario_ended and step < max_steps:
            step += 1
            
            chosen_action = self.tuned_decision(sim.state)
            
            allowed, _ = is_action_allowed(chosen_action, sim.state)
            if not allowed:
                chosen_action = Action.CALL_FOR_HELP
            
            sim.apply_action(chosen_action)
            
            if sim.state.user_urgency == 0 or sim.state.is_battery_depleted():
                break
        
        summary = sim.get_summary()
        success = summary['user_helped'] and not summary['battery_depleted']
        
        status = "SUCCESS" if success else "FAILED"
        tag = "success" if success else "failure"
        self.log(f"Result: {status} - Battery: {summary['final_battery']}%, Steps: {summary['total_steps']}\n", tag)
        
        return {'success': success, 'battery': summary['final_battery'], 'steps': summary['total_steps']}
    
    def reset_defaults(self):
        """Reset parameters to defaults."""
        self.params['recharge_threshold'].set(30)
        self.params['critical_battery'].set(15)
        self.params['help_min_battery'].set(20)
        self.params['safety_weight'].set(0.4)
        self.params['helpfulness_weight'].set(0.6)
        self.params['proactive_recharge'].set(False)
        self.params['risk_tolerance'].set("Medium")
        self.log("\nReset to default parameters.\n", "info")
    
    def export_code(self):
        """Export current parameters and write to implementation files."""
        params = {k: v.get() for k, v in self.params.items()}
        
        # Generate decision.py with tuned logic
        decision_code = self.generate_decision_code(params)
        scoring_code = self.generate_scoring_code(params)
        
        # Write to files
        try:
            with open('implementation/decision.py', 'w') as f:
                f.write(decision_code)
            
            with open('implementation/scoring.py', 'w') as f:
                f.write(scoring_code)
            
            self.output_text.delete(1.0, tk.END)
            self.log("Successfully Updated Implementation Files!\n", "success")
            self.log("=" * 60 + "\n\n", "header")
            self.log("The following parameters have been written to:\n", "info")
            self.log("- implementation/decision.py\n", "info")
            self.log("- implementation/scoring.py\n\n", "info")
            
            self.log("Tuned Parameters:\n", "header")
            self.log(f"  Recharge Threshold: {params['recharge_threshold']}%\n", "info")
            self.log(f"  Critical Battery: {params['critical_battery']}%\n", "info")
            self.log(f"  Help Min Battery: {params['help_min_battery']}%\n", "info")
            self.log(f"  Safety Weight: {params['safety_weight']:.2f}\n", "info")
            self.log(f"  Helpfulness Weight: {params['helpfulness_weight']:.2f}\n", "info")
            self.log(f"  Proactive Recharge: {params['proactive_recharge']}\n", "info")
            self.log(f"  Risk Tolerance: {params['risk_tolerance']}\n\n", "info")
            
            self.log("You can now run the main GUI to test these settings!\n", "success")
            self.log("Run: python main.py\n", "info")
            
        except Exception as e:
            self.log(f"Error writing files: {str(e)}\n", "failure")
    
    def generate_decision_code(self, params):
        """Generate decision.py code with tuned parameters."""
        buffer = 1.5 if params['risk_tolerance'] == "Conservative" else (0.7 if params['risk_tolerance'] == "Aggressive" else 1.0)
        
        return f'''"""
Decision-making logic for the assistive robot.

This file has been auto-generated by the Parameter Tuning GUI.
Tuned parameters are embedded in the decision logic below.
"""

from core.actions import Action
from core.state import RobotState
from core.constraints import is_action_allowed

# TUNED PARAMETERS
RECHARGE_THRESHOLD = {params['recharge_threshold']}
CRITICAL_BATTERY = {params['critical_battery']}
HELP_MIN_BATTERY = {params['help_min_battery']}
PROACTIVE_RECHARGE = {params['proactive_recharge']}
RISK_BUFFER = {buffer:.1f}  # Based on {params['risk_tolerance']} risk tolerance


def choose_action(state: RobotState) -> Action:
    """
    Choose the best action based on tuned parameters.
    
    This implementation uses parameters tuned via the GUI to make decisions.
    """
    
    # Rule 1: Critical battery - must recharge or call for help
    if state.battery < CRITICAL_BATTERY:
        if state.user_urgency >= 3 and state.battery >= 10:
            return Action.HELP_USER
        elif state.battery >= 10:
            return Action.RECHARGE
        else:
            return Action.CALL_FOR_HELP
    
    # Rule 2: High urgency - help if we have enough battery
    if state.user_urgency >= 2 and state.battery >= HELP_MIN_BATTERY:
        return Action.HELP_USER
    
    # Rule 3: Battery below threshold - recharge
    if state.battery < RECHARGE_THRESHOLD * RISK_BUFFER:
        if PROACTIVE_RECHARGE or state.user_urgency == 0:
            return Action.RECHARGE
    
    # Rule 4: Any urgency with decent battery - help
    if state.user_urgency >= 1 and state.battery >= HELP_MIN_BATTERY:
        return Action.HELP_USER
    
    # Rule 5: No urgency - maintain battery
    if state.battery < RECHARGE_THRESHOLD:
        return Action.RECHARGE
    
    # Default - wait
    return Action.WAIT


def evaluate_options(state: RobotState) -> dict[Action, float]:
    """Evaluate all actions and return their scores."""
    # Could implement scoring here if needed
    return {{}}
'''
    
    def generate_scoring_code(self, params):
        """Generate scoring.py code with tuned parameters."""
        return f'''"""
Action scoring and evaluation system.

This file has been auto-generated by the Parameter Tuning GUI.
Tuned parameters are embedded in the scoring logic below.
"""

from core.actions import Action
from core.state import RobotState

# TUNED PARAMETERS
SAFETY_WEIGHT = {params['safety_weight']:.2f}
HELPFULNESS_WEIGHT = {params['helpfulness_weight']:.2f}
CRITICAL_BATTERY = {params['critical_battery']}
RECHARGE_THRESHOLD = {params['recharge_threshold']}
HELP_MIN_BATTERY = {params['help_min_battery']}


def score_action(action: Action, state: RobotState) -> float:
    """
    Evaluate how good an action is in the current state.
    
    This implementation uses tuned weights to balance safety and helpfulness.
    """
    
    safety_score = score_safety(action, state)
    helpfulness_score = score_helpfulness(action, state)
    
    # Weighted combination using tuned weights
    total = safety_score * SAFETY_WEIGHT + helpfulness_score * HELPFULNESS_WEIGHT
    
    return total


def score_safety(action: Action, state: RobotState) -> float:
    """Score based on safety (battery management)."""
    score = 50.0
    
    if action == Action.HELP_USER:
        # Penalize helping when battery is low
        if state.battery < CRITICAL_BATTERY:
            score -= 100
        elif state.battery < HELP_MIN_BATTERY:
            score -= 50
        elif state.battery < RECHARGE_THRESHOLD:
            score -= 20
        else:
            score += 30
    
    elif action == Action.RECHARGE:
        # Reward recharging based on need
        if state.battery < CRITICAL_BATTERY:
            score += 100
        elif state.battery < RECHARGE_THRESHOLD:
            score += 70
        elif state.battery < 60:
            score += 30
        else:
            score -= 10
    
    elif action == Action.WAIT:
        score -= 20  # Generally discourage waiting
    
    elif action == Action.CALL_FOR_HELP:
        score += 10  # Safe but not preferred
    
    return score


def score_helpfulness(action: Action, state: RobotState) -> float:
    """Score based on helpfulness to user."""
    score = 0.0
    
    urgency_multiplier = [0, 1.5, 3.0, 5.0]
    
    if action == Action.HELP_USER:
        base_score = 100
        score = base_score * urgency_multiplier[state.user_urgency]
        
        # Bonus for good battery
        if state.battery > RECHARGE_THRESHOLD:
            score += 40
    
    elif action == Action.RECHARGE:
        score = 20  # Necessary but delays help
        
        if state.user_urgency >= 3:
            score -= 80  # Bad to delay critical help
        elif state.user_urgency >= 2:
            score -= 40
        
        # But necessary if low battery
        if state.battery < CRITICAL_BATTERY:
            score += 60
    
    elif action == Action.WAIT:
        if state.user_urgency == 0:
            score = 10
        else:
            score = -50  # Bad to wait when user needs help
    
    elif action == Action.CALL_FOR_HELP:
        if state.user_urgency >= 2:
            score = 30
        else:
            score = -30
    
    return score


def score_efficiency(action: Action, state: RobotState) -> float:
    """Score based on efficiency."""
    # Optional: implement efficiency scoring
    return 0.0
'''
    
    def log(self, text, tag=None):
        """Log text to output."""
        if tag:
            self.output_text.insert(tk.END, text, tag)
        else:
            self.output_text.insert(tk.END, text)
        self.output_text.see(tk.END)
        self.root.update_idletasks()


def main():
    root = tk.Tk()
    app = TuningGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
