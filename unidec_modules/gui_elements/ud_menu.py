import wx


class main_menu(wx.Menu):
    def __init__(self, parent, config, pres, tabbed):
        super(wx.Menu, self).__init__()
        self.pres = pres
        self.config = config
        self.parent = parent
        self.tabbed = tabbed


        self.filemenu = wx.Menu()
        self.toolsmenu = wx.Menu()
        self.analysismenu = wx.Menu()
        self.advancedmenu = wx.Menu()
        self.experimentalmenu = wx.Menu()

        # File Menu
        self.menuOpen = self.filemenu.Append(wx.ID_OPEN, "Open File\tCtrl+O", " Open a Text File in x y text, mzML, or Thermo RAW format")
        self.menuOpenRaw = self.filemenu.Append(wx.ID_ANY, "Open Waters Raw File", " Open a Waters .Raw File")
        self.filemenu.AppendSeparator()

        self.menuLoadState = self.filemenu.Append(wx.ID_ANY, "Load State\tCtrl+L", "Load state from folder")
        self.menuSaveState = self.filemenu.Append(wx.ID_ANY, "Save State\tCtrl+S", "Save program state to fresh folder")
        self.filemenu.AppendSeparator()

        self.menupastespectrum = self.filemenu.Append(wx.ID_ANY, "Get Spectrum From Clipboard\tCtrl+G",
                                                      "Pastes the spectrum, formats, and loads")
        self.filemenu.AppendSeparator()

        self.menuLoad = self.filemenu.Append(wx.ID_ANY, "Load External Config File", "Load in a configuration file")
        self.menuLoadDefault = self.filemenu.Append(wx.ID_ANY, "Load Default Config File",
                                                    "Load in default configuration file")
        self.menuSaveDefault = self.filemenu.Append(wx.ID_ANY, "Save Default Config File",
                                                    "Save default configuration file")

        # Default Submenu
        self.defaultmenu = wx.Menu()
        self.menuDefault0 = self.defaultmenu.Append(999, "Low-resolution Native",
                                                    "General factory defaults for low-resolution native MS")
        self.menuDefault1 = self.defaultmenu.Append(1000, "High-resolution Native",
                                                    "Defaults for high-resolution data (Exactive EMR).")
        self.menuDefault2 = self.defaultmenu.Append(1001, "Zero-Charge Mass Deisotoping",
                                                    "Defaults for loading zero-charge mass spectrum as output")
        self.menuDefault3 = self.defaultmenu.Append(1002, "Isotopic Resolution",
                                                    "Defaults for isotopically resolved data.")
        self.menuDefault4 = self.defaultmenu.Append(1003, "Nanodiscs",
                                                    "Defaults for POPC Nanodiscs.")
        self.filemenu.Append(wx.ID_ANY, "Presets", self.defaultmenu)
        self.filemenu.AppendSeparator()

        self.menufigdialog = self.filemenu.Append(wx.ID_ANY, "Save Figure As",
                                                  "Dialog to define path and extension for figure saving")
        # Figure Submenu
        self.figmenu = wx.Menu()

        self.menuSaveFigure0 = self.figmenu.Append(wx.ID_ANY, "Save Figures as .pdf", "Save all figures to .pdf format")
        self.menuSaveFigure1s = self.figmenu.Append(wx.ID_ANY, "Save Figures as PDF thumbnail",
                                                    "Save all figures to small PDF format")
        self.menuSaveFigure1 = self.figmenu.Append(wx.ID_ANY, "Save Figures as .eps", "Save all figures to .eps format")
        self.menuSaveFigure2 = self.figmenu.Append(wx.ID_ANY, "Save Figures as .png", "Save all figures to .png format")
        if self.config.imflag == 0:
            self.menuSaveFigure4 = self.figmenu.Append(wx.ID_ANY, "Generate PDF Report", "Generate PDF Report")
        else:
            self.menuSaveFigure4 = self.figmenu.Append(wx.ID_ANY, "Save Figures as .pdf",
                                                       "Save all figures to .pdf format")
        self.filemenu.Append(wx.ID_ANY, 'Save Figure Presets', self.figmenu)
        self.filemenu.AppendSeparator()

        self.menuAbout = self.filemenu.Append(wx.ID_ABOUT, "&About", " Information about this program")
        self.menuExit = self.filemenu.Append(wx.ID_EXIT, "E&xit\tCtrl+Q", " Terminate the Program")

        # Setting Up the Tools Menu


        self.menuBatch = self.toolsmenu.Append(wx.ID_ANY, "Batch Process\tCtrl+B",
                                               "Run these conditions on multiple samples")
        self.menuBatch2 = self.toolsmenu.Append(wx.ID_ANY, "Batch Process - Independent Data Ranges",
                                                "Run these conditions with varying preset data ranges on multiple samples")
        self.toolsmenu.AppendSeparator()

        self.menuBatchRaw = self.toolsmenu.Append(wx.ID_ANY, "Simple Batch Process Raw To Txt",
                                                  "Batch convert .raw to .txt files with default parameters")
        self.menuImportWizard = self.toolsmenu.Append(wx.ID_ANY, "Raw to Txt Conversion Wizard",
                                                      "Batch convert .raw to .txt files with wizard")
        self.toolsmenu.AppendSeparator()

        self.menuAutoWidth = self.toolsmenu.Append(wx.ID_ANY, "Automatic Peak Width\tCtrl+W",
                                                   "Try to get peak width automatically.")
        self.menuWidth = self.toolsmenu.Append(wx.ID_ANY, "Peak Width Tool", "Help determine the peak width")
        self.toolsmenu.AppendSeparator()

        self.menuManualFile = self.toolsmenu.Append(wx.ID_ANY, "Manual Assignment",
                                                    "Manually set UniDec to preassign specific m/z values")
        self.toolsmenu.AppendSeparator()

        self.menuMassFile = self.toolsmenu.Append(wx.ID_ANY, "Oligomer and Mass Tools\tCtrl+T",
                                                  "Oligomer and Mass Tools")

        # Setting up Analysis Menu
        self.menuPlotZ = self.analysismenu.Append(wx.ID_ANY, "Native Charge/Mass Tools",
                                                  "Tool for exploring relationship between charge and native mass and extraction specific distributions")
        self.analysismenu.AppendSeparator()

        self.menucollect = self.analysismenu.Append(wx.ID_ANY, "Data Collector Utility",
                                                    "Collect results and extract values.  Experimental KD fitting.")
        self.analysismenu.AppendSeparator()

        self.menuExport = self.analysismenu.Append(wx.ID_ANY, "Export Peaks Parameters and Data",
                                                   "Export intensities of charge states, areas, average charge state, and other parameters for the peaks")
        self.menuFitNorm = self.analysismenu.Append(wx.ID_ANY, "Fit Peak Intensities",
                                                    "Fits masses and reports normalized and relative peak intensities")
        self.analysismenu.AppendSeparator()

        self.menukendrick = self.analysismenu.Append(wx.ID_ANY, "Kendrick Mass Tools\tCtrl+K", "Kendrick Mass Analysis")
        self.menufft = self.analysismenu.Append(wx.ID_ANY, "FFT Window")
        self.parent.Bind(wx.EVT_MENU, self.pres.on_fft_window, self.menufft)
        self.menu2Dgrid = self.analysismenu.Append(wx.ID_ANY, "2D Grid Analysis", "2D Grid Analysis")
        self.menuautocorr = self.analysismenu.Append(wx.ID_ANY, "Autocorrelation",
                                                     "Autocorrelation of Mass Distribution")
        self.analysismenu.AppendSeparator()

        self.menuintegrate = self.analysismenu.Append(wx.ID_ANY, "Integrate Peaks\tCtrl+I",
                                                      "Peak area with range set by Peak Detection Range or Integration Range")
        self.menumatch = self.analysismenu.Append(wx.ID_ANY, "Auto Match Peaks\tCtrl+M",
                                                  "Run \"Match to Mixed Oligomers\" in Oligomer and Mass Tools")
        self.analysismenu.AppendSeparator()

        self.menucom = self.analysismenu.Append(wx.ID_ANY, "Report Center of Mass",
                                                "Reports center of mass for the zoomed region of the zero-charge mass spectrum")
        self.analysismenu.AppendSeparator()

        self.menuchargeplot = self.analysismenu.Append(wx.ID_ANY, "Plot By Charge",
                                                       "Plots Mass Distributions as a Function of Charge")
        self.menuoffset = self.analysismenu.Append(wx.ID_ANY, "Plot Charge Offsets\tCtrl+F",
                                                   "Plots Mass vs. Charge Offset in 2D Plot")

        if self.config.imflag == 1:
            self.analysismenu.AppendSeparator()
            self.menuimtools = self.analysismenu.Append(wx.ID_ANY, "IM Parameters Tool",
                                                        "Tools for estimating IM parameters.")
            self.menuimtools2 = self.analysismenu.Append(wx.ID_ANY, "IM Extraction Tool",
                                                         "Tools for Extraction IM Results.")
            self.menunativeccs = self.analysismenu.Append(wx.ID_ANY, "Plot Predicted Native CCS",
                                                          "Plot Predicted Native CCS values on mass vs ccs plot.")
            self.parent.Bind(wx.EVT_MENU, self.pres.on_im_tools, self.menuimtools)
            self.parent.Bind(wx.EVT_MENU, self.pres.on_im_extract, self.menuimtools2)
            self.parent.Bind(wx.EVT_MENU, self.pres.on_plot_nativeccs, self.menunativeccs)

        # Setting up the Advanced Menu
        self.menuReset = self.advancedmenu.Append(wx.ID_ANY, "Reset To Factory Default", "Reset Parameters to Default")
        self.advancedmenu.AppendSeparator()

        self.menuUnidecPath = self.advancedmenu.Append(wx.ID_FILE1, "UniDec File", "Find the UniDec executable file.")
        self.menuFileName = self.advancedmenu.Append(wx.ID_FILE2, "Rename Files",
                                                     "Rename the files into and out of UniDec.")
        self.menuOpenDir = self.advancedmenu.Append(wx.ID_ANY, "Open Saved File Directory",
                                                    "Opens the save directory in the file explorer")

        if self.config.imflag == 0:
            self.advancedmenu.AppendSeparator()
            self.advancedmenu.Append(401, "Best Mode", "Best UniDec Deconvolution Algorithm", wx.ITEM_RADIO)
            self.advancedmenu.Append(402, "Auto Baseline", "Experimental version with automatic baseline fitting",
                                     wx.ITEM_RADIO)
            self.advancedmenu.Append(403, "Auto Baseline Subtract", "Experimental version with automatic baseline subtraction", wx.ITEM_RADIO)
            self.parent.Bind(wx.EVT_MENU, self.menu_401_403, id=401)
            self.parent.Bind(wx.EVT_MENU, self.menu_401_403, id=402)
            self.parent.Bind(wx.EVT_MENU, self.menu_401_403, id=403)

        self.advancedmenu.AppendSeparator()

        self.scalemenu = wx.Menu()

        self.scalemenu.Append(501, "Linear", "Normal linear intensity scale", wx.ITEM_RADIO)
        self.scalemenu.Append(502, "Logarithmic", "Logarithmic intensity scale",
                              wx.ITEM_RADIO)
        self.scalemenu.Append(503, "Square Root", "Square root intensity scale", wx.ITEM_RADIO)
        self.parent.Bind(wx.EVT_MENU, self.menu_501_503, id=501)
        self.parent.Bind(wx.EVT_MENU, self.menu_501_503, id=502)
        self.parent.Bind(wx.EVT_MENU, self.menu_501_503, id=503)

        self.advancedmenu.Append(wx.ID_ANY, 'Intensity Scale', self.scalemenu)
        self.advancedmenu.AppendSeparator()

        if self.config.imflag == 0:
            self.menuflipmode = self.advancedmenu.Append(wx.ID_ANY, "Switch to Ion Mobility Mode",
                                                         "Switch interface to IM-MS Mode.")
        else:
            self.menuflipmode = self.advancedmenu.Append(wx.ID_ANY, "Switch to 1D Mass Spec Mode",
                                                         "Switch interface to MS Mode.")
        if self.tabbed == 0:
            self.menufliptabbed = self.advancedmenu.Append(wx.ID_ANY, "Switch to Tabbed Plots Mode",
                                                           "Put plots in individual tabs.")
        else:
            self.menufliptabbed = self.advancedmenu.Append(wx.ID_ANY, "Switch to Single Plot Window",
                                                           "Put plots in single large window.")

        # Experimental Menu
        self.menuundo = self.experimentalmenu.Append(wx.ID_ANY, "Undo Parameter Change\tCtrl+Z",
                                                     "Go back to the previous set of parameters")
        self.menuredo = self.experimentalmenu.Append(wx.ID_ANY, "Redo Parameter Change\tCtrl+Y",
                                                     "Go to the next set of parameters")
        self.experimentalmenu.AppendSeparator()
        self.Tweet = self.experimentalmenu.Append(wx.ID_ANY, "Twitter", "Twitter Extension")
        if self.config.imflag == 0:
            self.experimentalmenu.AppendSeparator()
            self.menuAdditionalParameters = self.experimentalmenu.Append(wx.ID_ANY, "Additional Parameters",
                                                                         "Adjust some experimental parameters")
            self.experimentalmenu.AppendSeparator()
            # self.menuMinimize = self.experimentalmenu.Append(wx.ID_ANY, "Minimize", "Minimize Peak List")
            # self.experimentalmenu.AppendSeparator()
            self.menuDeisotope = self.experimentalmenu.Append(wx.ID_ANY, "Load Zero-Charge Mass Spectrum",
                                                              "Load Zero-Charge Mass as input spectrum. Useful for deisotoping.")
            self.experimentalmenu.AppendSeparator()
            self.menuCrossValidate = self.experimentalmenu.Append(wx.ID_ANY, "Cross Validate",
                                                                  "Estimate errors through cross validation.")
            self.experimentalmenu.AppendSeparator()
            self.menucolor1d = self.experimentalmenu.Append(wx.ID_ANY, "Color Plots",
                                                            "Make a Different Colored 1D Plot")
            self.parent.Bind(wx.EVT_MENU, self.pres.on_zerocharge_mass, self.menuDeisotope)
            self.parent.Bind(wx.EVT_MENU, self.pres.on_cross_validate, self.menuCrossValidate)
            self.parent.Bind(wx.EVT_MENU, self.pres.on_additional_parameters, self.menuAdditionalParameters)
            self.parent.Bind(wx.EVT_MENU, self.pres.on_color_plot1d, self.menucolor1d)
            # self.parent.Bind(wx.EVT_MENU, self.pres.on_minimize, self.menuMinimize)
        self.experimentalmenu.AppendSeparator()

        self.menusuperbatch = self.experimentalmenu.Append(wx.ID_ANY, "Speed Batch",
                                                           "Minimal Batch Run, only writing config and calling program.")
        self.experimentalmenu.AppendSeparator()

        self.menumassprocess = self.experimentalmenu.Append(wx.ID_ANY, "Process Zero-Charge Mass Spectrum",
                                                            "Apply smoothing, background subtraction, and intensity threshold to zero-charge mass spectrum")
        self.experimentalmenu.AppendSeparator()

        self.menuerrors = self.experimentalmenu.Append(wx.ID_ANY, "Get Errors")
        self.menucal = self.experimentalmenu.Append(wx.ID_ANY, "Apply Calibration")
        self.parent.Bind(wx.EVT_MENU, self.pres.on_calibrate, self.menucal)
        self.experimentalmenu.AppendSeparator()

        self.menugriddecon = self.experimentalmenu.Append(wx.ID_ANY, "Grid Deconvolution")
        self.parent.Bind(wx.EVT_MENU, self.pres.on_grid_decon, self.menugriddecon)

        self.menuhdf5 = self.experimentalmenu.Append(wx.ID_ANY, "Write HDF5")
        self.parent.Bind(wx.EVT_MENU, self.pres.on_write_hdf5, self.menuhdf5)

        self.experimentalmenu.AppendSeparator()
        self.autoformat = self.experimentalmenu.Append(wx.ID_ANY, "Auto Format Monomer/Dimer",
                                                       "Mark matched monomers and dimers automatically")
        self.parent.Bind(wx.EVT_MENU, self.pres.on_autoformat, self.autoformat)

        self.experimentalmenu.AppendSeparator()
        self.menulauncher = self.experimentalmenu.Append(wx.ID_ANY, "Launcher")
        self.parent.Bind(wx.EVT_MENU, self.pres.on_launcher, self.menulauncher)

        # Set Events for Menu Bar

        # File Menu
        self.parent.Bind(wx.EVT_MENU, self.pres.on_open, self.menuOpen)
        self.parent.Bind(wx.EVT_MENU, self.pres.on_raw_open, self.menuOpenRaw)
        self.parent.Bind(wx.EVT_MENU, self.pres.on_load_state, self.menuLoadState)
        self.parent.Bind(wx.EVT_MENU, self.pres.on_save_state, self.menuSaveState)
        self.parent.Bind(wx.EVT_MENU, self.pres.on_paste_spectrum, self.menupastespectrum)
        self.parent.Bind(wx.EVT_MENU, self.pres.on_load_conf_file, self.menuLoad)
        self.parent.Bind(wx.EVT_MENU, self.pres.on_save_default, self.menuSaveDefault)
        self.parent.Bind(wx.EVT_MENU, self.pres.on_load_default, self.menuLoadDefault)
        self.parent.Bind(wx.EVT_MENU, self.on_defaults, self.menuDefault0)
        self.parent.Bind(wx.EVT_MENU, self.on_defaults, self.menuDefault1)
        self.parent.Bind(wx.EVT_MENU, self.on_defaults, self.menuDefault2)
        self.parent.Bind(wx.EVT_MENU, self.on_defaults, self.menuDefault3)
        self.parent.Bind(wx.EVT_MENU, self.on_defaults, self.menuDefault4)
        self.parent.Bind(wx.EVT_MENU, self.parent.on_save_figure_dialog, self.menufigdialog)
        self.parent.Bind(wx.EVT_MENU, self.parent.on_save_figure_pdf, self.menuSaveFigure0)
        self.parent.Bind(wx.EVT_MENU, self.parent.on_save_figure_eps, self.menuSaveFigure1)
        self.parent.Bind(wx.EVT_MENU, self.parent.on_save_figure_small, self.menuSaveFigure1s)
        self.parent.Bind(wx.EVT_MENU, self.parent.on_save_figure_png, self.menuSaveFigure2)
        self.parent.Bind(wx.EVT_MENU, self.parent.pres.on_pdf_report, self.menuSaveFigure4)
        self.parent.Bind(wx.EVT_MENU, self.parent.on_about, self.menuAbout)
        self.parent.Bind(wx.EVT_MENU, self.parent.on_exit, self.menuExit)

        # Tools

        self.parent.Bind(wx.EVT_MENU, self.pres.on_import_wizard, self.menuImportWizard)
        self.parent.Bind(wx.EVT_MENU, self.pres.on_mass_tools, self.menuMassFile)
        self.parent.Bind(wx.EVT_MENU, self.pres.on_batch, self.menuBatch)
        self.parent.Bind(wx.EVT_MENU, self.pres.on_batch2, self.menuBatch2)
        self.parent.Bind(wx.EVT_MENU, self.pres.on_batch_raw, self.menuBatchRaw)
        self.parent.Bind(wx.EVT_MENU, self.pres.on_peak_width_tool, self.menuWidth)
        self.parent.Bind(wx.EVT_MENU, self.pres.on_auto_peak_width, self.menuAutoWidth)
        self.parent.Bind(wx.EVT_MENU, self.pres.on_manual, self.menuManualFile)
        self.parent.Bind(wx.EVT_MENU, self.pres.on_undo, self.menuundo)
        self.parent.Bind(wx.EVT_MENU, self.pres.on_redo, self.menuredo)

        # Analysis
        self.parent.Bind(wx.EVT_MENU, self.pres.on_nativez_tools, self.menuPlotZ)
        self.parent.Bind(wx.EVT_MENU, self.pres.on_data_collector, self.menucollect)
        self.parent.Bind(wx.EVT_MENU, self.pres.on_export_params, self.menuExport)
        self.parent.Bind(wx.EVT_MENU, self.pres.on_fit_masses, self.menuFitNorm)
        self.parent.Bind(wx.EVT_MENU, self.pres.on_plot_offsets, self.menuoffset)
        self.parent.Bind(wx.EVT_MENU, self.pres.on_charge_plot, self.menuchargeplot)
        self.parent.Bind(wx.EVT_MENU, self.pres.on_center_of_mass, self.menucom)
        self.parent.Bind(wx.EVT_MENU, self.pres.on_integrate, self.menuintegrate)
        self.parent.Bind(wx.EVT_MENU, self.pres.on_2d_grid, self.menu2Dgrid)
        self.parent.Bind(wx.EVT_MENU, self.pres.on_kendrick, self.menukendrick)
        self.parent.Bind(wx.EVT_MENU, self.pres.on_autocorr_window, self.menuautocorr)
        self.parent.Bind(wx.EVT_MENU, self.pres.on_match, self.menumatch)

        # Advanced
        self.parent.Bind(wx.EVT_MENU, self.pres.on_reset, self.menuReset)
        self.parent.Bind(wx.EVT_MENU, self.pres.on_unidec_path, self.menuUnidecPath)
        self.parent.Bind(wx.EVT_MENU, self.pres.on_file_name, self.menuFileName)
        self.parent.Bind(wx.EVT_MENU, self.parent.on_open_dir, self.menuOpenDir)
        self.parent.Bind(wx.EVT_MENU, self.pres.on_flip_tabbed, self.menufliptabbed)
        self.parent.Bind(wx.EVT_MENU, self.pres.on_flip_mode, self.menuflipmode)

        # Experimental
        self.parent.Bind(wx.EVT_MENU, self.pres.on_peak_errors, self.menuerrors)
        self.parent.Bind(wx.EVT_MENU, self.pres.on_tweet, self.Tweet)
        self.parent.Bind(wx.EVT_MENU, self.pres.on_mass_process, self.menumassprocess)
        self.parent.Bind(wx.EVT_MENU, self.pres.on_super_batch, self.menusuperbatch)

        # Setting Menu Bar
        self.menuBar = wx.MenuBar()
        self.menuBar.Append(self.filemenu, "&File")
        self.menuBar.Append(self.toolsmenu, "Tools")
        self.menuBar.Append(self.analysismenu, "Analysis")
        self.menuBar.Append(self.advancedmenu, "Advanced")
        self.menuBar.Append(self.experimentalmenu, "Experimental")
        #self.Append(self.filemenu, "&File")
        #self.Append(self.toolsmenu, "Tools")
        #self.Append(self.analysismenu, "Analysis")
        #self.Append(self.advancedmenu, "Advanced")
        #self.Append(self.experimentalmenu, "Experimental")
        pass

    def on_defaults(self, e):
        """
        Resets the configuration to a default predefined in the unidecstructure file.
        :param e: Menu event
        :return: None
        """
        nid = e.GetId() % 100
        if nid == 0:
            self.config.default_high_res()
        elif nid == 1:
            self.config.default_zero_charge()
        elif nid == 2:
            self.config.default_isotopic_res()
        elif nid == 3:
            self.config.default_nanodisc()
        elif nid == 99:
            self.config.default_decon_params()
        self.pres.import_config(None)

    def menu_401_403(self, event):
        """
        Menu function to adjust the UniDec core function (agreesiveflag).
        :param event: wx Event
        :return: None
        """
        event_id = event.GetId()
        if event_id == 401:
            self.config.aggressiveflag = 0
        if event_id == 402:
            self.config.aggressiveflag = 1
        if event_id == 403:
            self.config.aggressiveflag = 2
        print self.config.aggressiveflag

    def menu_501_503(self, event):
        """
        Menu function to adjust the intensity scale.
        :param event: wx Event
        :return: None
        """
        event_id = event.GetId()
        if event_id == 501:
            self.config.intscale = "Linear"
        if event_id == 502:
            self.config.intscale = "Logarithmic"
        if event_id == 503:
            self.config.intscale = "Square Root"
        print self.config.intscale
