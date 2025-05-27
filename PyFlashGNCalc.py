import wx               # WXPython library
import math             # Math library
import gettext          # GetText library
_ = gettext.gettext

# Number validator - to validate user input
class NumericValidator(wx.Validator):
    # Setup
    def __init__(self):
        super().__init__()
        # Event Bind
        self.Bind(wx.EVT_CHAR, self.OnChar)
        # Avoid spamming popups
        self.ShowWarning = False

    # If character is cloned
    def Clone(self):
        return NumericValidator()

    # Get validation state
    def Validate(self, win):
        return True

    # Get which character was pressed
    def OnChar(self, event):
        # Get a key which was pressed
        key = event.GetKeyCode()
        char = chr(key) if 32 <= key <= 255 else ''
        # Defined allowed character
        allowed = "0123456789.,"

        # Check if only allowed character was pressed
        if char and char not in allowed:
            if not self.ShowWarning:
                wx.MessageBox(
                    "Only numbers, a dot (.) or a comma (,) are allowed.",
                    "Invalid Input",
                    wx.OK | wx.ICON_WARNING
                )
                self.ShowWarning = True

            return  # Block the key

        # Show warning to false
        self.ShowWarning = False
        event.Skip()

# Main Frame class
class MainFrame ( wx.Frame ):

    # Main frame setup with app title + size
    def __init__( self, parent ):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = _(u"Flash GN Calculator"),
                            pos = wx.DefaultPosition, size = wx.Size( 500,325 ),
                            style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

        # Set app size
        self.SetSizeHints( wx.Size( 500,325 ), wx.Size( 500,325 ) )

        # Icon setup
        BMP = wx.Bitmap("fgnc.png", wx.BITMAP_TYPE_PNG)
        Icon = wx.Icon()
        Icon.CopyFromBitmap(BMP)
        self.SetIcon(Icon)

        # Main app sizer
        VB_MainSizer = wx.BoxSizer( wx.VERTICAL )

        # Calculate WX panel setup
        self.WP_CalculaterPanel = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )

        # Calculate horizontal box setup
        HB_CalculatePanel = wx.BoxSizer( wx.HORIZONTAL )

        # Static box for Calculate setup
        SBH_CalculateSizer = wx.StaticBoxSizer( wx.StaticBox( self.WP_CalculaterPanel, wx.ID_ANY, _(u"Calculate") ),
                                                wx.HORIZONTAL )

        # Guide number Radio button setup
        self.RBtn_GN = wx.RadioButton( SBH_CalculateSizer.GetStaticBox(), wx.ID_ANY, _(u"Guide Number (GN)"),
                                       wx.DefaultPosition, wx.DefaultSize, 0 )
        SBH_CalculateSizer.Add( self.RBtn_GN, 0, wx.ALL, 5 )

        # F number Radio button setup
        self.RBtn_F = wx.RadioButton( SBH_CalculateSizer.GetStaticBox(), wx.ID_ANY, _(u"F-Number"),
                                      wx.DefaultPosition, wx.DefaultSize, 0 )
        SBH_CalculateSizer.Add( self.RBtn_F, 0, wx.ALL, 5 )

        # Distance Radio button setup
        self.RBtn_Distance = wx.RadioButton( SBH_CalculateSizer.GetStaticBox(), wx.ID_ANY, _(u"Distance"),
                                             wx.DefaultPosition, wx.DefaultSize, 0 )
        SBH_CalculateSizer.Add( self.RBtn_Distance, 0, wx.ALL, 5 )

        # StaticBox of Calculate add to Calculate HorizontalBox
        HB_CalculatePanel.Add( SBH_CalculateSizer, 1, wx.ALL|wx.EXPAND, 5 )

        # Static box setup for Unit selection
        SBH_UnitsSizer = wx.StaticBoxSizer( wx.StaticBox( self.WP_CalculaterPanel, wx.ID_ANY, _(u"Units") ),
                                            wx.HORIZONTAL )

        # Meters Radio button setup
        self.RBtn_Meters = wx.RadioButton( SBH_UnitsSizer.GetStaticBox(), wx.ID_ANY, _(u"Meters"),
                                           wx.DefaultPosition, wx.DefaultSize, 0 )
        SBH_UnitsSizer.Add( self.RBtn_Meters, 0, wx.ALL, 5 )

        # Feet Radio button setup
        self.RBtn_Feet = wx.RadioButton( SBH_UnitsSizer.GetStaticBox(), wx.ID_ANY, _(u"Feet"),
                                         wx.DefaultPosition, wx.DefaultSize, 0 )
        SBH_UnitsSizer.Add( self.RBtn_Feet, 0, wx.ALL, 5 )

        # StaticBox of Units add to Calculate HorizontalBox
        HB_CalculatePanel.Add( SBH_UnitsSizer, 0, wx.ALL|wx.EXPAND, 5 )

        # Calculate panel setup
        self.WP_CalculaterPanel.SetSizer( HB_CalculatePanel )
        self.WP_CalculaterPanel.Layout()

        # Calculate panel add to HorizontalBox
        HB_CalculatePanel.Fit( self.WP_CalculaterPanel )

        # Calculate panel add to Main sizer
        VB_MainSizer.Add( self.WP_CalculaterPanel, 0, wx.EXPAND, 5 )

        # Parameters WX panel setup
        self.WP_ParametersPanel = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        VB_Parameters = wx.BoxSizer( wx.VERTICAL )

        # Parameters StaticBox sizer setup
        SBV_ParametersSizer = wx.StaticBoxSizer( wx.StaticBox( self.WP_ParametersPanel, wx.ID_ANY,
                                                               _(u"Parameters") ), wx.VERTICAL )
        # ISO HorizontalBox setup
        HB_ISO = wx.BoxSizer( wx.HORIZONTAL )

        # Text label ISO
        self.Txt_ISO = wx.StaticText( SBV_ParametersSizer.GetStaticBox(), wx.ID_ANY, _(u"ISO:"),
                                      wx.DefaultPosition, wx.DefaultSize, 0 )
        self.Txt_ISO.Wrap( -1 )

        # Text label add to ISO HorizontalBox
        HB_ISO.Add( self.Txt_ISO, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

        # noinspection PyTypeChecker
        HB_ISO.Add( ( 118, 0), 0, wx.EXPAND, 5 )

        # TextControl for ISO setup
        self.TxtCTRL_ISO = wx.TextCtrl( SBV_ParametersSizer.GetStaticBox(), wx.ID_ANY,
                                        wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        HB_ISO.Add( self.TxtCTRL_ISO, 1, wx.ALL|wx.EXPAND, 5 )

        # StaticBox sizer add to ISO HorizontalBox
        SBV_ParametersSizer.Add( HB_ISO, 0, wx.EXPAND, 5 )

        self.Splitter_ISO_F_Distance = wx.StaticLine( SBV_ParametersSizer.GetStaticBox(), wx.ID_ANY,
                                                      wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
        SBV_ParametersSizer.Add( self.Splitter_ISO_F_Distance, 0, wx.EXPAND |wx.ALL, 5 )

        # F-Number HorizontalBox setup
        HB_FNumber = wx.BoxSizer( wx.HORIZONTAL )

        # Text label F-Number
        self.Txt_F = wx.StaticText( SBV_ParametersSizer.GetStaticBox(), wx.ID_ANY, _(u"F-Number (aperture):"),
                                    wx.DefaultPosition, wx.DefaultSize, 0 )
        self.Txt_F.Wrap( -1 )

        # Text label add to F-Number HorizontalBox
        HB_FNumber.Add( self.Txt_F, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

        # noinspection PyTypeChecker
        HB_FNumber.Add( ( 26, 0), 0, wx.EXPAND, 5 )

        # TextControl for F-Number setup
        self.TxtCTRL_F = wx.TextCtrl( SBV_ParametersSizer.GetStaticBox(), wx.ID_ANY, wx.EmptyString,
                                      wx.DefaultPosition, wx.DefaultSize, 0 )
        HB_FNumber.Add( self.TxtCTRL_F, 1, wx.ALL|wx.EXPAND, 5 )

        # StaticBox add to F-Number HorizontalBox
        SBV_ParametersSizer.Add( HB_FNumber, 1, wx.EXPAND, 5 )

        # Distance HorizontalBox setup
        HB_Distance = wx.BoxSizer( wx.HORIZONTAL )

        # Text label Distance
        self.Txt_Distance = wx.StaticText( SBV_ParametersSizer.GetStaticBox(), wx.ID_ANY, _(u"Distance "
                                                                                            u"(flash to subject):"),
                                           wx.DefaultPosition, wx.DefaultSize, 0 )
        self.Txt_Distance.Wrap( -1 )

        # Text label add to Distance HorizontalBox
        HB_Distance.Add( self.Txt_Distance, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

        # TextControl for Distance setup
        self.TxtCTRL_Distance = wx.TextCtrl( SBV_ParametersSizer.GetStaticBox(), wx.ID_ANY, wx.EmptyString,
                                             wx.DefaultPosition, wx.DefaultSize, 0 )
        HB_Distance.Add( self.TxtCTRL_Distance, 1, wx.ALL|wx.EXPAND, 5 )

        # StaticBox add to Distance HorizontalBox
        SBV_ParametersSizer.Add( HB_Distance, 1, wx.EXPAND, 5 )

        # StaticBox add to Parameters VerticalBox
        VB_Parameters.Add( SBV_ParametersSizer, 1, wx.EXPAND|wx.ALL, 5 )

        # Parameters panel setup
        self.WP_ParametersPanel.SetSizer( VB_Parameters )
        self.WP_ParametersPanel.Layout()

        # Parameters panel add to VerticalBox
        VB_Parameters.Fit( self.WP_ParametersPanel )

        # Parameters panel add to Main sizer
        VB_MainSizer.Add( self.WP_ParametersPanel, 0, wx.EXPAND, 5 )

        # Help WX panel setup
        self.WP_HelpPanel = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )

        # Help VerticalBox setup
        VB_Help = wx.BoxSizer( wx.VERTICAL )

        # Text of Help
        self.Txt_Help = wx.StaticText( self.WP_HelpPanel, wx.ID_ANY, _(u"Distance is from flash to subject.\nUnits can"
                                                                       u" be meters or feet - stay consistent.\nGuide "
                                                                       u"number should be entered as if for ISO 100"
                                                                       u" - ISO will adjust automatically."),
                                       wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL )
        self.Txt_Help.Wrap( -1 )

        # Text of Help add to Help VerticalBox
        VB_Help.Add( self.Txt_Help, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )

        # Help panel setup
        self.WP_HelpPanel.SetSizer( VB_Help )
        self.WP_HelpPanel.Layout()

        # Help panel add to VerticalBox
        VB_Help.Fit( self.WP_HelpPanel )

        # Help panel add to Main sizer
        VB_MainSizer.Add( self.WP_HelpPanel, 0, wx.EXPAND, 5 )

        # Results WX panel setup
        self.WP_ResultsPanel = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )

        # Results VerticalBox setup
        VB_Results = wx.BoxSizer( wx.VERTICAL )

        # Text of Results
        self.Txt_Results = wx.StaticText( self.WP_ResultsPanel, wx.ID_ANY, _(u"Results: "), wx.DefaultPosition,
                                          wx.DefaultSize, 0 )
        self.Txt_Results.Wrap( -1 )

        # Results text stilling
        self.Txt_Results.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL,
                                           wx.FONTWEIGHT_BOLD, False, wx.EmptyString ) )

        # Text of Results add to Results VerticalBox
        VB_Results.Add( self.Txt_Results, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )

        # Results panel setup
        self.WP_ResultsPanel.SetSizer( VB_Results )
        self.WP_ResultsPanel.Layout()

        # Results panel add to VerticalBox
        VB_Results.Fit( self.WP_ResultsPanel )

        # Help panel add to Main sizer
        VB_MainSizer.Add( self.WP_ResultsPanel, 1, wx.EXPAND, 5 )

        # Main Frame final setup
        self.SetSizer( VB_MainSizer )
        self.Layout()
        self.Centre( wx.BOTH )

        # Bind radio buttons for mode
        self.RBtn_GN.Bind(wx.EVT_RADIOBUTTON, self.OnModeChange)
        self.RBtn_F.Bind(wx.EVT_RADIOBUTTON, self.OnModeChange)
        self.RBtn_Distance.Bind(wx.EVT_RADIOBUTTON, self.OnModeChange)

        # Bind radio buttons for units
        self.RBtn_Meters.Bind(wx.EVT_RADIOBUTTON, self.OnUnitChange)
        self.RBtn_Feet.Bind(wx.EVT_RADIOBUTTON, self.OnUnitChange)

        # Bind input fields
        self.TxtCTRL_F.Bind(wx.EVT_TEXT, self.Calculate)
        self.TxtCTRL_Distance.Bind(wx.EVT_TEXT, self.Calculate)
        self.TxtCTRL_ISO.Bind(wx.EVT_TEXT, self.Calculate)

        # Apply validator
        self.TxtCTRL_F.SetValidator(NumericValidator())
        self.TxtCTRL_Distance.SetValidator(NumericValidator())
        self.TxtCTRL_ISO.SetValidator(NumericValidator())

        # Set defaults
        self.RBtn_GN.SetValue(True)
        self.RBtn_Meters.SetValue(True)

        # Initial calculation
        self.OnModeChange(None)

    # Clean Up any mess
    def __del__( self ):
        pass

    # Detect in which mode we are and change Text accordingly
    def OnModeChange(self, event):
        # Get value based on which RadioButton is pressed
        if self.RBtn_GN.GetValue():                                                             # Guide Number RButton
            self.Txt_F.SetLabel("F-Number (aperture):")
            self.TxtCTRL_F.SetToolTip("Lens aperture (e.g., 2.8, 5.6, 8)")
            self.Txt_Distance.SetLabel("Distance (flash to subject):")
            self.TxtCTRL_Distance.SetToolTip("Distance from flash to subject")
        elif self.RBtn_F.GetValue():                                                            # F-Number RButton
            self.Txt_F.SetLabel("Guide Number (ISO 100):")
            self.TxtCTRL_F.SetToolTip("Flash's GN at ISO 100 (adjusted for selected ISO)")
            self.Txt_Distance.SetLabel("Distance (flash to subject):")
            self.TxtCTRL_Distance.SetToolTip("Distance from flash to subject")
        else:                                                                                   # Last RButton pressed
            self.Txt_F.SetLabel("Guide Number (ISO 100):")
            self.TxtCTRL_F.SetToolTip("Flash's GN at ISO 100 (adjusted for selected ISO)")
            self.Txt_Distance.SetLabel("F-Number (aperture):")
            self.TxtCTRL_Distance.SetToolTip("Lens aperture (e.g., 2.8, 5.6, 8)")

        # Set Calculate function to none
        self.Calculate(None)

    # Get if we changed units from "Meters" to "Feet"
    def OnUnitChange(self, event):
        self.Calculate(None)

    # Calculate ISO factor from our ISO TextControl
    def GetISOFactor(self):
        try:
            ISO_STR = self.TxtCTRL_ISO.GetValue().replace(",", ".")
            ISO = float(ISO_STR)
            if ISO <= 0:
                return 1.0
            return math.sqrt(ISO / 100)
        except ValueError:
            return 1.0

    # Distance conversion from "Meters" to "Feet"
    def ConvertDistance(self, value):
        if self.RBtn_Feet.GetValue():
            return value * 0.3048  # feet → meters
        return value  # already in meters

    # Parse float for replacement of "," or "." - MultiCultyShit
    @staticmethod
    def ParseFloat(value):
        try:
            return float(value.replace(",", "."))
        except ValueError:
            return None

    # Calculate results based on source data
    def Calculate(self, event):
        Value1 = self.ParseFloat(self.TxtCTRL_F.GetValue())
        Value2 = self.ParseFloat(self.TxtCTRL_Distance.GetValue())

        # Check if our 2 Values are valid or not
        if Value1 is None or Value2 is None:
            self.Txt_Results.SetLabel("Result: Please enter valid numbers.")
            return

        # Get ISO from GetISOFactor function
        ISO_Factor = self.GetISOFactor()

        # Determine selected mode
        if self.RBtn_GN.GetValue():  # Calculate GN
            Distance = self.ConvertDistance(Value2)
            Result = Value1 * Distance * ISO_Factor
            self.Txt_Results.SetLabel(f"Result: Guide Number = {Result:.2f}")

        elif self.RBtn_F.GetValue():  # Calculate F-Number
            Distance = self.ConvertDistance(Value2)
            if Distance == 0:
                self.Txt_Results.SetLabel("Result: Distance can't be zero.")
                return
            GN_Adjusted = Value1 * ISO_Factor
            Result = GN_Adjusted / Distance
            self.Txt_Results.SetLabel(f"Result: F-Number = {Result:.2f}")

        else:  # Calculate Distance
            if Value2 == 0:
                self.Txt_Results.SetLabel("Result: F-Number can't be zero.")
                return
            GN_Adjusted = Value1 * ISO_Factor
            Distance = GN_Adjusted / Value1
            if self.RBtn_Feet.GetValue():
                Distance /= 0.3048
                self.Txt_Results.SetLabel(f"Result: Distance = {Distance:.2f} ft")
            else:
                self.Txt_Results.SetLabel(f"Result: Distance = {Distance:.2f} m")

    # Close app + Confirm dialog
    def OnClose(self, event):

        # Small confirm dialog setup
        dlg = wx.MessageDialog(
            self,
            "Are you sure you want to quit?",
            "Quit PyUInstaller",
            wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION
        )

        # Show dialog
        result = dlg.ShowModal()
        dlg.Destroy()

        # If Pressed yes in dialog close app
        if result == wx.ID_YES:
            # Close app
            self.Destroy()

# Main App loop
app = wx.App(False)
frame = MainFrame(None)
frame.Show()
frame.Bind(wx.EVT_CLOSE, frame.OnClose)  # Bind for CloseEvent
app.MainLoop()