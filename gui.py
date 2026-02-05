"""
GUI for the Assistive Robot Decision-Making System.

This provides a visual interface to:
- Configure and run scenarios quickly
- Visualize decisions in real-time
- Compare performance metrics
- Export results
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from typing import Optional, Callable
import json
from pathlib import Path
from dataclasses import replace

from core.state import RobotState
from core.actions import Action
from core.simulator import RobotSimulator
from implementation.decision import choose_action as impl_choose_action
from solutions.solution_decision import choose_action as solution_choose_action
from core.constraints import is_action_allowed, get_constraint_warnings
from core.metrics import PerformanceMetrics


class ToggleSwitch(tk.Canvas):
    """
    Custom toggle switch widget with modern design.
    
    A visual toggle button that switches between two states (ON/OFF) with
    smooth animations and clear visual feedback. Used to switch between
    different AI implementations in the GUI.
    
    Attributes:
        width (int): Width of the toggle switch in pixels
        height (int): Height of the toggle switch in pixels
        on_text (str): Text displayed when switch is ON
        off_text (str): Text displayed when switch is OFF
        command (callable): Callback function called when switch is toggled
        state (bool): Current state (True=ON, False=OFF)
    """
    
    def __init__(self, parent, width=180, height=50, on_text="Custom Implementation", 
                 off_text="Reference Solution", command=None, **kwargs):
        # Get parent bg safely, fallback to system default
        try:
            parent_bg = parent.cget('bg')
        except:
            parent_bg = 'SystemButtonFace'
        
        super().__init__(parent, width=width, height=height, bg=parent_bg, 
                        highlightthickness=0, **kwargs)
        
        self.width = width
        self.height = height
        self.on_text = on_text
        self.off_text = off_text
        self.command = command
        self.state = False  # False = off, True = on
        
        # Colors
        self.on_color = "#4CAF50"    # Green
        self.off_color = "#FF9800"   # Orange
        self.slider_color = "#FFFFFF"  # White
        self.text_color = "#FFFFFF"  # White
        
        # Animation
        self.animation_steps = 10
        self.animation_speed = 20  # ms
        
        # Bind click event
        self.bind("<Button-1>", self.toggle)
        
        # Draw initial state
        self.draw()
    
    def draw(self):
        """
        Draw the toggle switch in its current state.
        
        Renders the background, text label, and slider circle based on
        the current state (ON or OFF).
        """
        self.delete("all")
        
        # Determine current colors and position
        if self.state:
            bg_color = self.on_color
            text = self.on_text
            slider_x = self.width - 35
        else:
            bg_color = self.off_color
            text = self.off_text
            slider_x = 15
        
        # Draw background rounded rectangle
        self.create_rounded_rect(5, 5, self.width-5, self.height-5, 20, 
                                fill=bg_color, outline="")
        
        # Draw text
        self.create_text(self.width/2, self.height/2, text=text, 
                        fill=self.text_color, font=("Arial", 11, "bold"))
        
        # Draw slider circle
        self.create_oval(slider_x-15, 10, slider_x+15, self.height-10,
                        fill=self.slider_color, outline="", tags="slider")
    
    def create_rounded_rect(self, x1, y1, x2, y2, radius, **kwargs):
        """
        Draw a rounded rectangle on the canvas.
        
        Args:
            x1: Left x-coordinate
            y1: Top y-coordinate
            x2: Right x-coordinate
            y2: Bottom y-coordinate
            radius: Corner radius in pixels
            **kwargs: Additional canvas drawing options (fill, outline, etc.)
            
        Returns:
            Canvas object ID of the created polygon
        """
        points = [
            x1+radius, y1,
            x2-radius, y1,
            x2, y1,
            x2, y1+radius,
            x2, y2-radius,
            x2, y2,
            x2-radius, y2,
            x1+radius, y2,
            x1, y2,
            x1, y2-radius,
            x1, y1+radius,
            x1, y1
        ]
        return self.create_polygon(points, smooth=True, **kwargs)
    
    def toggle(self, event=None):
        """
        Toggle the switch state and execute callback.
        
        Args:
            event: Optional Tkinter event object (from click binding)
        """
        self.state = not self.state
        self.draw()
        
        # Call callback if provided
        if self.command:
            self.command()
    
    def set_state(self, state: bool):
        """
        Set the switch state programmatically.
        
        Args:
            state: New state (True=ON, False=OFF)
        """
        if self.state != state:
            self.state = state
            self.draw()
    
    def get_state(self) -> bool:
        """
        Get the current state of the toggle switch.
        
        Returns:
            bool: Current state (True=ON, False=OFF)
        """
        return self.state


class RobotSimulatorGUI:
    """
    Main GUI application for the Assistive Robot Decision-Making System.
    
    Provides an interactive interface for running and comparing AI implementations
    through various test scenarios. Features include:
    - Toggle between custom implementation and reference solution
    - 12 preset scenarios with different challenge levels
    - Real-time simulation output with color-coded results
    - Performance metrics and comparative analysis
    - Export functionality for results and metrics
    
    Attributes:
        root: Tkinter root window
        current_scenario: Currently selected scenario configuration
        all_results (list): List of results from all executed scenarios
        metrics: PerformanceMetrics object for calculating statistics
        use_solution (bool): Whether to use reference solution (False=custom impl)
    """
    
    def __init__(self, root):
        self.root = root
        self.root.title("Assistive Robot Decision-Making System - Simulator")
        self.root.geometry("1200x800")
        
        # Configure style
        style = ttk.Style()
        style.theme_use('clam')
        
        # Data storage
        self.current_scenario = None
        self.all_results = []
        self.metrics = PerformanceMetrics()
        self.use_solution = False  # Toggle between implementation and solution
        
        # Create main layout
        self.create_layout()
        
        # Load default scenario
        self.load_default_scenario()
    
    def create_layout(self):
        """
        Create the main GUI layout with all panels and controls.
        
        Sets up a two-column layout:
        - Left panel: Scenario selection and controls
        - Right panel: Simulation output display
        """
        
        # Main container with padding
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights for resizing
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(0, weight=1)
        
        # Left panel - Scenarios
        self.create_scenarios_panel(main_frame)
        
        # Right panel - Output and visualization
        self.create_output_panel(main_frame)
    
    def create_scenarios_panel(self, parent):
        """
        Create the scenarios selection panel with controls.
        
        Includes:
        - AI implementation toggle switch
        - Quick action buttons (Run All, Clear, Export, Compare)
        - 12 individual preset scenario buttons
        
        Args:
            parent: Parent Tkinter widget to place this panel in
        """
        scenarios_frame = ttk.LabelFrame(parent, text="Run Scenarios", padding="10")
        scenarios_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 5))
        
        # AI Implementation toggle
        toggle_frame = ttk.Frame(scenarios_frame)
        toggle_frame.grid(row=0, column=0, columnspan=2, pady=(0, 15))
        
        ttk.Label(toggle_frame, text="AI Implementation:", 
                 font=('TkDefaultFont', 10, 'bold')).pack(pady=(0, 8))
        
        # Create modern toggle switch
        self.impl_toggle = ToggleSwitch(
            toggle_frame,
            width=200,
            height=50,
            on_text="Custom Implementation",
            off_text="Reference Solution",
            command=self.toggle_implementation
        )
        self.impl_toggle.pack()
        self.impl_toggle.set_state(True)  # Start with "Custom Implementation" (ON)
        
        # Separator
        ttk.Separator(scenarios_frame, orient=tk.HORIZONTAL).grid(row=1, column=0, columnspan=2, 
                                                                  sticky=(tk.W, tk.E), pady=(10, 15))
        
        # Action buttons
        ttk.Label(scenarios_frame, text="Quick Actions:", 
                 font=('TkDefaultFont', 9, 'bold')).grid(row=2, column=0, columnspan=2, 
                                                         sticky=tk.W, pady=(0, 5))
        
        ttk.Button(scenarios_frame, text="Run All Scenarios", 
                  command=self.run_all_scenarios,
                  width=30).grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=2)
        
        ttk.Button(scenarios_frame, text="Clear Output", 
                  command=self.clear_output,
                  width=30).grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=2)
        
        ttk.Button(scenarios_frame, text="Export Results", 
                  command=self.export_results,
                  width=30).grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=2)
        
        ttk.Button(scenarios_frame, text="Compare Performance", 
                  command=self.compare_implementations,
                  width=30).grid(row=6, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=2)
        
        # Separator
        ttk.Separator(scenarios_frame, orient=tk.HORIZONTAL).grid(row=7, column=0, columnspan=2, 
                                                                  sticky=(tk.W, tk.E), pady=(10, 10))
        
        # Preset scenarios
        ttk.Label(scenarios_frame, text="Individual Scenarios:", 
                 font=('TkDefaultFont', 9, 'bold')).grid(row=8, column=0, columnspan=2, 
                                                         sticky=tk.W, pady=(0, 5))
        
        # Define preset scenarios with more variety
        self.presets = [
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
        
        # Create buttons for each preset
        for i, (name, state, max_steps) in enumerate(self.presets):
            ttk.Button(scenarios_frame, text=name, 
                      command=lambda n=name, s=state, m=max_steps: self.run_single_scenario(n, s, m),
                      width=30).grid(row=9+i, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=1)
    
    def create_output_panel(self, parent):
        """
        Create the output and visualization panel.
        
        Displays simulation results in a scrollable text area with
        color-coded tags for different message types (success, failure, warning).
        
        Args:
            parent: Parent Tkinter widget to place this panel in
        """
        output_frame = ttk.LabelFrame(parent, text="Simulation Output", padding="10")
        output_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        output_frame.columnconfigure(0, weight=1)
        output_frame.rowconfigure(0, weight=1)
        
        # Output text area - make it larger
        self.output_text = scrolledtext.ScrolledText(output_frame, wrap=tk.WORD, 
                                                      width=80, height=40, 
                                                      font=('Courier', 9))
        self.output_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure tags for colored output
        self.output_text.tag_config("header", foreground="#0066cc", font=('Courier', 9, 'bold'))
        self.output_text.tag_config("success", foreground="#009900")
        self.output_text.tag_config("failure", foreground="#cc0000")
        self.output_text.tag_config("warning", foreground="#ff8800")
        self.output_text.tag_config("action", foreground="#0066cc", font=('Courier', 9, 'bold'))
    
    
    def toggle_implementation(self):
        """
        Toggle between custom implementation and reference solution.
        
        Updates the internal state and logs the change to the output panel.
        Note: The toggle switch state is inverted (ON=Your Impl, OFF=Solution).
        """
        # The toggle switch state is inverted: ON=Your Impl, OFF=Solution
        self.use_solution = not self.impl_toggle.get_state()
        
        if self.use_solution:
            self.log_output("\n[INFO] Switched to Reference Solution\n", "header")
        else:
            self.log_output("\n[INFO] Switched to Custom Implementation\n", "header")
    
    # Scenario management
    def load_default_scenario(self):
        """
        Load the default scenario and display welcome message.
        
        Called during initialization to set up the initial state.
        """
        self.log_output("Ready to run scenarios. Select a scenario from the list.\n", "header")
    
    def run_single_scenario(self, name: str, initial_state: RobotState, max_steps: int):
        """
        Run a single preset scenario with the selected AI implementation.
        
        Args:
            name: Human-readable name of the scenario
            initial_state: Starting robot state configuration
            max_steps: Maximum number of simulation steps allowed
        """
        # Create a fresh copy of the state to avoid mutation issues
        state_copy = replace(initial_state)
        result = self.execute_scenario(name, state_copy, max_steps)
        self.all_results.append(result)
        self.metrics.add_scenario(result)
        self.log_output("\n", "header")
    
    def run_all_scenarios(self):
        """
        Run all 12 preset scenarios sequentially and display summary.
        
        Clears previous results, executes each scenario, collects metrics,
        and displays a comprehensive summary table at the end.
        """
        self.clear_results()
        
        for name, state, max_steps in self.presets:
            # Create a fresh copy of the state to avoid mutation issues
            state_copy = replace(state)
            result = self.execute_scenario(name, state_copy, max_steps)
            self.all_results.append(result)
            self.metrics.add_scenario(result)
            self.log_output("\n" + "="*70 + "\n\n", "header")
        
        # Display summary
        self.display_summary()
    
    def execute_scenario(self, name: str, initial_state: RobotState, max_steps: int) -> dict:
        """
        Execute a scenario with detailed logging and return results.
        
        Runs the simulation step-by-step, displays decisions and outcomes,
        applies constraints, and logs all activity to the output panel.
        
        Args:
            name: Scenario name for display
            initial_state: Starting robot state
            max_steps: Maximum steps before timeout
            
        Returns:
            dict: Summary of scenario results including battery usage,
                  steps taken, success status, etc.
        """
        self.log_output(f"{'='*70}\n", "header")
        self.log_output(f"  Scenario: {name}\n", "header")
        self.log_output(f"{'='*70}\n", "header")
        self.log_output(f"Initial State: {initial_state}\n\n")
        
        # Store initial values
        initial_battery = initial_state.battery
        initial_urgency = initial_state.user_urgency
        
        sim = RobotSimulator(initial_state, max_steps)
        
        # Simulation loop
        step = 0
        while not sim.scenario_ended and step < max_steps:
            step += 1
            
            # AI chooses action (use selected implementation)
            if self.use_solution:
                chosen_action = solution_choose_action(sim.state)
            else:
                chosen_action = impl_choose_action(sim.state)
            
            # Check constraints
            allowed, reason = is_action_allowed(chosen_action, sim.state)
            warnings = get_constraint_warnings(chosen_action, sim.state)
            
            if not allowed:
                self.log_output(f"Step {step}: [BLOCKED] {chosen_action} — {reason}\n", "failure")
                chosen_action = Action.CALL_FOR_HELP
            
            # Display decision
            self.log_output(f"Step {step}: {sim.state}\n")
            self.log_output(f"  -> Decision: ", "action")
            self.log_output(f"{chosen_action}\n", "action")
            
            # Display warnings
            for warning in warnings:
                self.log_output(f"    {warning}\n", "warning")
            
            # Execute action
            result = sim.apply_action(chosen_action)
            self.log_output(f"    {result.message}\n")
            
            # Check for user success
            if sim.state.user_urgency == 0:
                self.log_output(f"\n[SUCCESS] User need fully resolved.\n", "success")
                break
            
            # Check for battery depletion
            if sim.state.is_battery_depleted():
                self.log_output(f"\n[FAILURE] Battery depleted!\n", "failure")
                break
        
        # Display summary
        summary = sim.get_summary()
        self.log_output(f"\n{'-'*70}\n")
        self.log_output("Scenario Summary:\n", "header")
        self.log_output(f"  Total steps: {summary['total_steps']}\n")
        self.log_output(f"  Final battery: {summary['final_battery']}%\n")
        self.log_output(f"  Final urgency: {summary['final_urgency']}\n")
        
        if summary['user_helped']:
            self.log_output(f"  User helped: Yes\n", "success")
        else:
            self.log_output(f"  User helped: No\n", "failure")
        
        if summary['battery_depleted']:
            self.log_output(f"  Battery depleted: Yes\n", "failure")
        else:
            self.log_output(f"  Battery depleted: No\n", "success")
        
        self.log_output(f"{'-'*70}\n")
        
        # Return results
        return {
            'name': name,
            'initial_battery': initial_battery,
            'initial_urgency': initial_urgency,
            'steps': summary['total_steps'],
            'final_battery': summary['final_battery'],
            'user_helped': summary['user_helped'],
            'battery_depleted': summary['battery_depleted'],
        }
    
    def display_summary(self):
        """
        Display a formatted summary table of all scenario results.
        
        Shows a table with scenario names, initial conditions, steps taken,
        final battery levels, and success/failure status.
        """
        if not self.all_results:
            return
        
        self.log_output("\n" + "="*70 + "\n", "header")
        self.log_output("  PERFORMANCE SUMMARY\n", "header")
        self.log_output("="*70 + "\n", "header")
        
        # Header
        header = f"{'Scenario':<25} {'Start':<12} {'Steps':<7} {'Battery':<9} {'Success':<9}"
        self.log_output(header + "\n")
        self.log_output("-"*70 + "\n")
        
        # Results
        total_success = 0
        total_failures = 0
        
        for result in self.all_results:
            name = result['name'][:23]
            start = f"B:{result['initial_battery']}% U:{result['initial_urgency']}"
            steps = str(result['steps'])
            battery = f"{result['final_battery']}%"
            success = "YES" if result['user_helped'] else "NO"
            
            line = f"{name:<25} {start:<12} {steps:<7} {battery:<9} {success:<9}"
            
            if result['battery_depleted']:
                self.log_output(line + " DEPLETED\n", "failure")
                total_failures += 1
            elif result['user_helped']:
                self.log_output(line + " OK\n", "success")
                total_success += 1
            else:
                self.log_output(line + " INCOMPLETE\n", "warning")
                total_failures += 1
        
        self.log_output("-"*70 + "\n")
        self.log_output(f"Overall: {total_success}/{len(self.all_results)} scenarios completed successfully\n", 
                       "header")
        self.log_output("="*70 + "\n", "header")
    
    
    # Output management
    def log_output(self, text: str, tag: Optional[str] = None):
        """
        Log text to the output display area with optional styling.
        
        Args:
            text: Text to display
            tag: Optional tag for styling (header, success, failure, warning, action)
        """
        if tag:
            self.output_text.insert(tk.END, text, tag)
        else:
            self.output_text.insert(tk.END, text)
        self.output_text.see(tk.END)
        self.root.update_idletasks()
    
    def clear_output(self):
        """
        Clear the output text area.
        
        Removes all displayed text from the simulation output panel.
        """
        self.output_text.delete(1.0, tk.END)
    
    def clear_results(self):
        """
        Clear all stored results and metrics.
        
        Resets the results list and metrics object, and clears the output display.
        """
        self.all_results = []
        self.metrics = PerformanceMetrics()
        self.clear_output()
    
    def export_results(self):
        """
        Export results and metrics to JSON files.
        
        Saves two files to the output/ directory:
        - gui_results.json: Scenario results data
        - gui_metrics.json: Calculated performance metrics
        
        Shows a confirmation dialog upon completion.
        """
        if not self.all_results:
            messagebox.showinfo("No Results", "No results to export. Run some scenarios first!")
            return
        
        # Create output directory if it doesn't exist
        output_dir = Path("output")
        output_dir.mkdir(exist_ok=True)
        
        # Save results
        results_file = output_dir / "gui_results.json"
        with open(results_file, 'w') as f:
            json.dump(self.all_results, f, indent=2)
        
        # Save metrics
        self.metrics.save_to_file("output/gui_metrics.json")
        
        messagebox.showinfo("Export Complete", 
                           f"Results exported to:\n- {results_file}\n- output/gui_metrics.json")
    
    def compare_implementations(self):
        """
        Compare performance between custom implementation and reference solution.
        
        Runs all scenarios twice (once with each implementation), calculates
        metrics for both, and displays a detailed side-by-side comparison
        showing which implementation performs better in each category.
        """
        self.clear_output()
        self.log_output("="*70 + "\n", "header")
        self.log_output("  PERFORMANCE COMPARISON: Implementation vs Solution\n", "header")
        self.log_output("="*70 + "\n\n", "header")
        
        # Run all scenarios with implementation
        self.log_output("Running CUSTOM IMPLEMENTATION on all scenarios...\n\n", "header")
        self.use_solution = False
        impl_results = []
        impl_metrics = PerformanceMetrics()
        
        for name, state, max_steps in self.presets:
            state_copy = replace(state)
            result = self.execute_scenario_silent(name, state_copy, max_steps)
            impl_results.append(result)
            impl_metrics.add_scenario(result)
        
        # Run all scenarios with solution
        self.log_output("\nRunning REFERENCE SOLUTION on all scenarios...\n\n", "header")
        self.use_solution = True
        solution_results = []
        solution_metrics = PerformanceMetrics()
        
        for name, state, max_steps in self.presets:
            state_copy = replace(state)
            result = self.execute_scenario_silent(name, state_copy, max_steps)
            solution_results.append(result)
            solution_metrics.add_scenario(result)
        
        # Display comparison
        self.display_comparison(impl_results, solution_results, impl_metrics, solution_metrics)
        
        # Reset to original setting
        self.use_solution = False
        self.impl_toggle.set_state(True)  # Reset to "Custom Implementation"
    
    def execute_scenario_silent(self, name: str, initial_state: RobotState, max_steps: int) -> dict:
        """
        Execute a scenario without logging output.
        
        Used for batch comparison runs where we only need the results,
        not the detailed step-by-step output.
        
        Args:
            name: Scenario name
            initial_state: Starting robot state
            max_steps: Maximum steps allowed
            
        Returns:
            dict: Scenario results summary
        """
        initial_battery = initial_state.battery
        initial_urgency = initial_state.user_urgency
        
        sim = RobotSimulator(initial_state, max_steps)
        
        step = 0
        while not sim.scenario_ended and step < max_steps:
            step += 1
            
            # AI chooses action
            if self.use_solution:
                chosen_action = solution_choose_action(sim.state)
            else:
                chosen_action = impl_choose_action(sim.state)
            
            # Check constraints
            allowed, reason = is_action_allowed(chosen_action, sim.state)
            
            if not allowed:
                chosen_action = Action.CALL_FOR_HELP
            
            # Execute action
            result = sim.apply_action(chosen_action)
            
            # Check for completion
            if sim.state.user_urgency == 0 or sim.state.is_battery_depleted():
                break
        
        summary = sim.get_summary()
        
        return {
            'name': name,
            'initial_battery': initial_battery,
            'initial_urgency': initial_urgency,
            'steps': summary['total_steps'],
            'final_battery': summary['final_battery'],
            'user_helped': summary['user_helped'],
            'battery_depleted': summary['battery_depleted'],
        }
    
    def display_comparison(self, impl_results, solution_results, impl_metrics, solution_metrics):
        """
        Display detailed side-by-side comparison of two implementations.
        
        Shows:
        - Scenario-by-scenario comparison table
        - Win/loss/tie counts
        - Metrics comparison across all dimensions
        - Overall winner determination
        
        Args:
            impl_results: List of results from custom implementation
            solution_results: List of results from reference solution
            impl_metrics: PerformanceMetrics object for custom implementation
            solution_metrics: PerformanceMetrics object for reference solution
        """
        self.log_output("="*70 + "\n", "header")
        self.log_output("  SCENARIO-BY-SCENARIO COMPARISON\n", "header")
        self.log_output("="*70 + "\n", "header")
        
        # Header
        header = f"{'Scenario':<25} {'Impl':<8} {'Soln':<8} {'Winner':<10}\n"
        self.log_output(header)
        self.log_output("-"*70 + "\n")
        
        impl_wins = 0
        solution_wins = 0
        ties = 0
        
        for impl_r, soln_r in zip(impl_results, solution_results):
            name = impl_r['name'][:23]
            impl_status = "PASS" if impl_r['user_helped'] and not impl_r['battery_depleted'] else "FAIL"
            soln_status = "PASS" if soln_r['user_helped'] and not soln_r['battery_depleted'] else "FAIL"
            
            # Determine winner
            impl_score = (impl_r['user_helped'] * 100 + impl_r['final_battery']) if not impl_r['battery_depleted'] else 0
            soln_score = (soln_r['user_helped'] * 100 + soln_r['final_battery']) if not soln_r['battery_depleted'] else 0
            
            if impl_score > soln_score:
                winner = "Impl"
                winner_tag = "success"
                impl_wins += 1
            elif soln_score > impl_score:
                winner = "Solution"
                winner_tag = "warning"
                solution_wins += 1
            else:
                winner = "Tie"
                winner_tag = None
                ties += 1
            
            line = f"{name:<25} {impl_status:<8} {soln_status:<8} "
            self.log_output(line)
            self.log_output(f"{winner:<10}\n", winner_tag)
        
        self.log_output("-"*70 + "\n")
        self.log_output(f"Implementation Wins: {impl_wins}  |  Solution Wins: {solution_wins}  |  Ties: {ties}\n", "header")
        self.log_output("="*70 + "\n\n", "header")
        
        # Detailed Metrics Comparison
        impl_metrics_data = impl_metrics.calculate_all_metrics()
        soln_metrics_data = solution_metrics.calculate_all_metrics()
        
        self.log_output("="*70 + "\n", "header")
        self.log_output("  DETAILED METRICS COMPARISON\n", "header")
        self.log_output("="*70 + "\n\n", "header")
        
        # Define metrics to display in order (matching test_comparison.py)
        metrics_list = [
            ('Task Completion', 'completion_score'),
            ('Battery Efficiency', 'battery_efficiency'),
            ('Urgency Response', 'urgency_response'),
            ('Risk Management', 'risk_score'),
            ('Overall Score', 'overall_score'),
        ]
        
        header = f"{'Metric':<25} {'Custom':<15} {'Solution':<15} {'Winner':<15}\n"
        self.log_output(header)
        self.log_output("-"*70 + "\n")
        
        for name, key in metrics_list:
            impl_val = impl_metrics_data.get(key, 0)
            soln_val = soln_metrics_data.get(key, 0)
            
            impl_str = f"{impl_val:>6.1f}%"
            soln_str = f"{soln_val:>6.1f}%"
            
            # Determine winner with margin
            if abs(impl_val - soln_val) < 0.5:
                winner = "Tie"
                winner_tag = None
            elif impl_val > soln_val:
                winner = f"Custom (+{impl_val - soln_val:.1f})"
                winner_tag = "success"
            else:
                winner = f"Solution (+{soln_val - impl_val:.1f})"
                winner_tag = "warning"
            
            line = f"{name:<25} {impl_str:<15} {soln_str:<15} "
            self.log_output(line)
            self.log_output(f"{winner:<15}\n", winner_tag)
        
        self.log_output("-"*70 + "\n")
        self.log_output("="*70 + "\n", "header")
        
        # Overall winner
        impl_overall = impl_metrics_data.get("overall_score", 0)
        soln_overall = soln_metrics_data.get("overall_score", 0)
        
        self.log_output("\n")
        if impl_overall > soln_overall:
            self.log_output(f"WINNER: CUSTOM IMPLEMENTATION ({impl_overall:.1f}% vs {soln_overall:.1f}%)\n", "success")
            self.log_output("Congratulations! The custom AI outperformed the reference solution!\n", "success")
        elif soln_overall > impl_overall:
            self.log_output(f"WINNER: REFERENCE SOLUTION ({soln_overall:.1f}% vs {impl_overall:.1f}%)\n", "warning")
            self.log_output("The reference solution performed better. Try improving the custom AI!\n", "warning")
        else:
            self.log_output(f"TIE: Both scored {impl_overall:.1f}%\n", "header")
            self.log_output("Both implementations performed equally well!\n", "header")
        
        self.log_output("="*70 + "\n\n", "header")


def main():
    """
    Launch the GUI application.
    
    Creates the Tkinter root window, initializes the RobotSimulatorGUI,
    and starts the main event loop.
    """
    root = tk.Tk()
    app = RobotSimulatorGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
