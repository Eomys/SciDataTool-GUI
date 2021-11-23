from PySide2.QtWidgets import QWidget

from ...GUI.WAxisSelector.Ui_WAxisSelector import Ui_WAxisSelector
from PySide2.QtCore import Signal
from ...Functions.Plot import unit_dict, axes_dict, fft_dict, ifft_dict


class WAxisSelector(Ui_WAxisSelector, QWidget):
    """Widget to select the axis to plot"""

    refreshNeeded = Signal()
    axisChanged = Signal()
    actionChanged = Signal()

    def __init__(self, parent=None):
        """Initialize the arguments, linking the buttons and setting up the UI

        Parameters
        ----------
        self : WAxisSelector
            a WAxisSelector object
        parent : QWidget
            The parent widget
        """

        # Build the interface according to the .ui file
        QWidget.__init__(self, parent)
        self.setupUi(self)

        self.name = "X"  # Name of the axis
        self.axes_list = list()  # List of the different axes of the DataND object

        self.axis_selected = "None"  # Name of the axis selected (time, angle...)
        self.unit = "None"  # Name of the unit of the axis (s,m...)
        self.b_filter.setDisabled(True)

        self.c_axis.currentTextChanged.connect(self.update_axis)
        self.c_action.currentTextChanged.connect(self.update_action)
        self.c_unit.currentTextChanged.connect(self.update_unit)

    def get_axes_name(self):
        """Method that return the axes that can be selected
        Parameters
        ----------
        self : WAxisSelector
            a WAxisSelector object
        Output
        ---------
        list
            name of the axes avalaible
        """
        return self.axes_list

    def get_axis_unit_selected(self):
        """Method that return the axis and the unit currently selected so that we can use it in the plot method
        Parameters
        ----------
        self : WAxisSelector
            a WAxisSelector object
        Output
        ---------
        string
            name of the current axis and unit selected in the right format
        """

        return self.axis_selected + "{" + self.unit + "}"

    # def get_current_axis_name(self):
    #     """Method that return the axis currently selected
    #     Parameters
    #     ----------
    #     self : WAxisSelector
    #         a WAxisSelector object
    #     Output
    #     ---------
    #     string
    #         name of the current axis selected
    #     """

    #     return self.c_axis.currentText()

    def get_current_action_name(self):
        """Method that return the action currently selected
        Parameters
        ----------
        self : WAxisSelector
            a WAxisSelector object
        Output
        ---------
        string
            name of the current action selected
        """
        return self.c_action.currentText()

    def get_axis_selected(self):
        """Method that return the name of the axis selected of the WAxisSelector
        Parameters
        ----------
        self : WAxisSelector
            a WAxisSelector object
        Output
        ---------
        string
            name of the axis selected
        """
        return self.axis_selected

    # def get_current_unit(self):
    #     """Method that return the unit currently selected
    #     Parameters
    #     ----------
    #     self : WAxisSelector
    #         a WAxisSelector object
    #     Output
    #     ---------
    #     string
    #         name of the current unit selected
    #     """

    #     return self.unit

    def remove_axis(self, axis_to_remove):
        """Method that remove a given axis from the axis ComboBox.
        Parameters
        ----------
        self : WAxisSelector
            a WAxisSelector object
        axis_to_remove : string
            name of the axis to remove from c_axis

        """
        if axis_to_remove in self.axes_list:
            axes_list = self.axes_list[:]  # Getting the axes available
            axes_list.remove(axis_to_remove)  # Removing the axis selected

            # Building the new ComboBox
            self.c_axis.blockSignals(True)
            self.c_axis.clear()

            for ax in axes_list:
                if ax in axes_dict:
                    self.c_axis.addItem(axes_dict[ax])
                else:
                    self.c_axis.addItem(ax)

            self.c_axis.blockSignals(False)

            self.update_axis()

    def set_axis(self, axis):
        """Method that will set the comboboxes to have the axis given as an input when calling the plot method (auto-plot).
        Parameters
        ----------
        self : WAxisSelector
            a WAxisSelector object
        axis : RequestedAxis
            axis that we want to have in the WAxisSelector
        """
        # Step 1 : Getting the name of the axis and selecting the right combobox (axis and action)
        axis_name = axis.name

        # If the axis is freqs or wavenumber, then we have to select time/angle and fft
        if axis_name in ifft_dict:

            # Selecting the right axis
            for i in range(self.c_axis.count()):
                self.c_axis.setCurrentIndex(i)
                if self.c_axis.currentText() == ifft_dict[axis_name]:
                    break

            self.update_axis()
            # Making sure that we select FFT
            self.c_action.setCurrentIndex(1)

        else:
            # Selecting the right axis
            for i in range(self.c_axis.count()):
                self.c_axis.setCurrentIndex(i)
                if self.c_axis.currentText() == axis_name:
                    break

            self.update_axis()

        self.update_action()

        # Step 2 : Recovering the unit and setting the combobox according to it
        self.c_unit.blockSignals(True)
        unit_name = axis.unit

        if unit_name in unit_dict:
            for i in range(self.c_unit.count()):
                self.c_unit.setCurrentIndex(i)
                if self.c_unit.currentText() == unit_name:
                    break

        self.c_unit.blockSignals(False)
        self.update_unit()

    def set_axis_options(self, data):
        """Method that will put the axes of data in the combobox of the widget
        Parameters
        ----------
        self : WAxisSelector
            a WAxisSelector object
        data : DataND
            A DataND object that we want to plot

        """
        self.c_axis.blockSignals(True)
        # Step 1 : Getting the name of the different axes of the DataND object
        self.axes_list = [axis.name for axis in data.get_axes()]

        # At least one axis must be selected => impossible to have none for X axis
        if self.name.lower() != "x":
            self.axes_list.insert(0, "None")

        # Step 2 : Replacing the items inside of the ComboBox with the axes recovered
        self.c_axis.clear()
        for ax in self.axes_list:
            if ax in axes_dict:
                self.c_axis.addItem(axes_dict[ax])
            else:
                self.c_axis.addItem(ax)

        self.c_axis.blockSignals(False)

        # Step 3 : Modifying axis_selected
        if self.c_axis.currentText() in [axes_dict[key] for key in axes_dict]:
            self.axis_selected = [key for key in axes_dict][
                [axes_dict[key] for key in axes_dict].index(self.c_axis.currentText())
            ]
        else:
            self.axis_selected = self.c_axis.currentText()

        self.c_axis.view().setMinimumWidth(max([len(ax) for ax in self.axes_list]) * 6)

    def set_name(self, axis_name):
        """Method to change of the label of the widget
        Parameters
        ----------
        self : WAxisSelector
            a WAxisSelector object
        axis_name : string
            string that we will use to set the in_name of the widget

        """

        self.name = axis_name
        self.in_name.setText(axis_name)

    def set_action(self, action):
        """Method that set the action of the WAxisSelector
        Parameters
        ----------
        self : WAxisSelector
            a WAxisSelector object
        action : string
            name of the new action"""

        action_list = [self.c_action.itemText(i) for i in range(self.c_action.count())]

        if action in action_list and action != "Filter":
            self.c_action.setCurrentIndex(action_list.index(action))

    def set_unit(self):
        """Method that update the unit comboxbox according to the axis selected in the other combobox.
           We can also give the axis selected and put its units inside the combobox
        Parameters
        ----------
        self : WAxisSelector
            a WAxisSelector object
        axis : string
            name of the axis that is selected
        """
        self.c_unit.blockSignals(True)
        # Adding the right units according to a dictionnary
        if self.axis_selected == "None":
            # If the axis is not selected, then we can not choose the unit
            self.c_unit.clear()
            self.c_unit.setDisabled(True)
        else:
            self.c_unit.setDisabled(False)
            self.c_unit.clear()

            # Adding the right unit according to the imported dictionary
            if self.axis_selected in unit_dict:
                self.c_unit.addItems(unit_dict[self.axis_selected])

            self.c_unit.view().setMinimumWidth(
                max([len(un) for un in unit_dict[self.axis_selected]]) * 6
            )
        self.c_unit.blockSignals(False)
        self.update_unit()

    def update(self, data, axis_name="X"):
        """Method used to update the widget by calling the other method for the label, the axes and the units
        Parameters
        ----------
        self : WAxisSelector
            a WAxisSelector object
        data : DataND
            A DataND object to plot
        axis_name : string
            string that will set the text of in_name (=name of the axis)
        """

        self.set_name(axis_name)
        self.set_axis_options(data)
        self.set_unit()

    def update_axis(self):
        """Method called when an axis is changed that change axis_selected, the units available and the action combobox.
        It will also emit a signal used in WAxisManager.
        Parameters
        ----------
        self : WAxisSelector
            a WAxisSelector object
        """

        self.c_action.setCurrentIndex(0)

        # Updating the units and the axis selected
        # Making sure that self.axis_selected is a "tag" and not a "label". Example : z instead of axial direction
        if self.c_axis.currentText() in [axes_dict[key] for key in axes_dict]:
            self.axis_selected = [key for key in axes_dict][
                [axes_dict[key] for key in axes_dict].index(self.c_axis.currentText())
            ]
        else:
            self.axis_selected = self.c_axis.currentText()

        self.set_unit()

        # Updating the action combobox
        # Handling specific case to disable certain parts of the GUI
        if self.c_axis.currentText() == "None":
            self.c_action.setDisabled(True)
        else:
            self.c_action.setDisabled(False)

        if self.axis_selected in fft_dict:
            action = ["None", "FFT", "Filter"]
            self.c_action.clear()
            self.c_action.addItems(action)

        else:
            action = ["None", "Filter"]
            self.c_action.clear()
            self.c_action.addItems(action)

        self.c_action.view().setMinimumWidth(max([len(ac) for ac in action]) * 6)

        # Emitting the signals
        self.refreshNeeded.emit()
        self.axisChanged.emit()

    def update_action(self):
        """Method called when an action is changed that will change axis_selected,
        update the units available and emit a signal.
        Parameters
        ----------
        self : WAxisSelector
            a WAxisSelector object

        """
        # If the action selected is filter, then we enable the button
        if self.c_action.currentText() == "Filter":
            self.b_filter.setDisabled(False)

        else:
            self.b_filter.setDisabled(True)

        # Converting the axes according to action selected if possible/necessary
        if self.c_action.currentText() == "FFT" and self.axis_selected in fft_dict:
            self.axes_list.insert(
                self.axes_list.index(self.axis_selected), fft_dict[self.axis_selected]
            )
            self.axes_list.remove(self.axis_selected)
            self.axis_selected = fft_dict[self.axis_selected]

        elif self.c_action.currentText() == "None" and self.axis_selected in ifft_dict:
            self.axes_list.insert(
                self.axes_list.index(self.axis_selected), ifft_dict[self.axis_selected]
            )
            self.axes_list.remove(self.axis_selected)
            self.axis_selected = ifft_dict[self.axis_selected]

        # Handling the case where axis_selected is updated but axes_list is not
        # We check if fft(axis_selected) is in the list and when it is the case we replace it by axis_selected
        if not self.axis_selected in self.axes_list:
            if fft_dict[self.axis_selected] in self.axes_list:
                self.axes_list.insert(
                    self.axes_list.index(fft_dict[self.axis_selected]),
                    self.axis_selected,
                )
                self.axes_list.remove(fft_dict[self.axis_selected])

        # Now that the quantiy has been updated according to the action, we can set the units and emit the signals
        self.set_unit()

        self.refreshNeeded.emit()
        self.actionChanged.emit()

    def update_unit(self):
        """Method called when a new unit is selected so that we can update self.unit
        Parameters
        ----------
        self : WAxisSelector
            a WAxisSelector object

        """
        self.unit = self.c_unit.currentText()
