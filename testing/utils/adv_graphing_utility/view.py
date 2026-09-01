from pathlib import Path
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

import dataset_operations as ds_op


class View:
    def __init__(self):
        self._root = tk.Tk()

        self._dataset_path = tk.StringVar()
        self._plottable_variables = tk.StringVar()
        self._dimensions = tk.StringVar()

        self._variable = tk.StringVar()
        self._axes_dimensions = {"x": tk.StringVar(), "y": tk.StringVar()}
        self._axes_bounds = {
            "x": (tk.IntVar(value=0), tk.IntVar(value=0)),
            "y": (tk.IntVar(value=0), tk.IntVar(value=0))
        }

        self._create()
        self._connect_vars()

        self._root.mainloop()

    def _create(self) -> None:
        self._root.title("Advanced Graphing Utility")
        self._root.geometry("720x480")

        self._elements = {}

        self._create_select_dataset_frame()
        self._create_select_variable_frame()
        self._create_assign_axes_frame()

    def _connect_vars(self) -> None:
        self._dataset_path.trace_add("write", self._on_dataset_path_set)
        self._plottable_variables.trace_add("write", self._on_plottable_variables_set)
        self._dimensions.trace_add("write", self._on_dimensions_set)

        self._variable.trace_add("write", self._on_variable_set)

        for axis_id, var in self._axes_dimensions.items():
            axis_set_callback = lambda *args, id=axis_id: self._on_axis_dimension_set(id)

            var.trace_add("write", axis_set_callback)

    def _create_select_dataset_frame(self) -> None:
        select_dataset_frame = tk.Frame(self._root)
        select_dataset_frame.pack(pady=16)
        self._elements["dataset"] = select_dataset_frame

        self._create_dataset_label()
        self._create_dataset_button()

    def _create_select_variable_frame(self) -> None:
        select_variable_frame = tk.Frame(self._root)
        select_variable_frame.pack(pady=16)

        # Make variable select label
        label = tk.Label(
            select_variable_frame,
            text="Select variable to plot:",
            wraplength=450
        )

        label.pack(padx=4, side="left")

        # Make variable select dropdown
        dropdown = ttk.Combobox(
            select_variable_frame,
            textvariable=self._variable,
            state="readonly"
        )
        
        dropdown.pack(padx=4, side="left")
        self._elements["variable_select_dropdown"] = dropdown

    def _create_assign_axes_frame(self) -> None:
        assign_axes_frame = tk.Frame(self._root)
        assign_axes_frame.pack(pady=16, expand=True, fill="both")
        self._elements["axes"] = assign_axes_frame

        x_axis_frame = self._make_axis_frame(
            self._elements["axes"], "Select X-Axis", "x"
        )
        y_axis_frame = self._make_axis_frame(
            self._elements["axes"], "Select Y-Axis", "y"
        )

        self._elements["x-axis"] = x_axis_frame
        self._elements["y-axis"] = y_axis_frame
    
    def _create_dataset_button(self) -> None:
        select_button = tk.Button(
            self._elements["dataset"],
            text="Select NetCDF Dataset",
            command=self._select_dataset_dialog
        )
        select_button.pack(padx=4, side="left")

    def _select_dataset_dialog(self) -> None:
        file_path = filedialog.askopenfilename(
            title="Select a NetCDF dataset",
            filetypes=[
                ("NetCDF files", "*.nc *.nc4"),
                ("All files", "*.*")
            ]
        )

        self._dataset_path.set(file_path)

    def _create_dataset_label(self) -> None:
        dataset_label = tk.Label(
            self._elements["dataset"],
            text="No file selected",
            wraplength=450
        )
        dataset_label.pack(padx=4, side="left")

        self._elements["dataset_label"] = dataset_label

    def _make_axis_frame(self, parent: tk.Frame, text: str, axis_id: str) -> tk.Frame:
        center_frame = tk.Frame(parent)
        stack_frame = tk.Frame(center_frame)

        center_frame.pack(padx=4, side="left", fill="both", expand=True)
        stack_frame.pack()

        self._create_axis_label(stack_frame, text)
        self._create_axis_dimension_select(stack_frame, axis_id)
        self._create_axis_dimension_bounds(stack_frame, axis_id)

        return stack_frame

    def _create_axis_label(self, parent: tk.Frame, text: str) -> None:
        self._dataset_label = tk.Label(
            parent,
            text=text,
            wraplength=450
        )
        self._dataset_label.pack(pady=8)

    def _create_axis_dimension_select(self, parent: tk.Frame, axis_id: str) -> None:
        dimension_select = ttk.Combobox(
            parent,
            textvariable=self._axes_dimensions[axis_id],
            state="readonly"
        )

        dimension_select.pack(pady=8)

        self._elements[f"{axis_id}_axis_dimension"] = dimension_select

    def _create_axis_dimension_bounds(self, parent: tk.Frame, axis_id: str) -> None:
        min_validate = self._root.register(
            lambda value:
                self._validate_integer(
                    value,
                    self._axes_bounds[axis_id][0],
                    self._axes_bounds[axis_id][1]
                )
        )
        max_validate = self._root.register(
            lambda value:
                self._validate_integer(
                    value,
                    self._axes_bounds[axis_id][0],
                    self._axes_bounds[axis_id][1]
                )
        )

        min_select = tk.Entry(
            parent, validate="key", validatecommand=(min_validate, "%P")
        )
        max_select = tk.Entry(
            parent, validate="key", validatecommand=(max_validate, "%P")
        )

        min_select.pack(padx=4, side="left")
        max_select.pack(padx=4, side="left")

    # - - - Setter Callbacks - - -
    
    def _on_dataset_path_set(self, *_) -> None:
        path_str = self._dataset_path.get()

        if path_str:
            text = Path(path_str).name
        else:
            text = "No file selected"

        try:
            self._plottable_variables.set(
                ",".join(ds_op.get_plottable_variables(path_str))
            )
        except Exception:
            self._plottable_variables.set("")

        self._elements["dataset_label"].config(text=text)

    def _on_plottable_variables_set(self, *_) -> None:
        vars_str = self._plottable_variables.get()

        if not vars_str:
            vars = []
        else:
            vars = vars_str.split(",")

        self._elements["variable_select_dropdown"]["values"] = vars

    def _on_variable_set(self, *_) -> None:
        dimensions = ds_op.get_dimensions(
            self._dataset_path.get(), self._variable.get()
        )

        self._dimensions.set(",".join(dimensions))

    def _on_dimensions_set(self, *_) -> None:
        dimensions = self._dimensions.get().split(",")
        
        self._elements["x_axis_dimension"]["values"] = dimensions
        self._elements["y_axis_dimension"]["values"] = dimensions

    def _on_axis_dimension_set(self, axis_id: str, *_) -> None:
        dimension = self._axes_dimensions[axis_id].get()

        dim_max = ds_op.get_dimension_size(self._dataset_path.get(), dimension) - 1

        self._axes_bounds[axis_id][1].set(dim_max)

    # - - - Validators - - -

    def _validate_integer(
            self, value: str, min_var: tk.IntVar, max_var: tk.IntVar
    ) -> bool:
        if value == "":
            return True

        try:
            int_value = int(value)

            if int_value < min_var.get():
                return False
            if int_value > max_var.get():
                return False

            return True

        except ValueError:
            return False
