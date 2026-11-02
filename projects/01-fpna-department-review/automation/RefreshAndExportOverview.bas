Attribute VB_Name = "RefreshAndExportOverview"
Option Explicit

Public Sub RefreshAndExportOverview()
    Dim overview As Worksheet
    Dim exportPath As Variant

    On Error GoTo HandleError
    Set overview = ThisWorkbook.Worksheets("Overview")

    ThisWorkbook.RefreshAll
    Application.CalculateFull

    exportPath = Application.GetSaveAsFilename( _
        InitialFileName:="fpna_overview.pdf", _
        FileFilter:="PDF Files (*.pdf), *.pdf")

    If VarType(exportPath) = vbBoolean Then Exit Sub

    overview.ExportAsFixedFormat _
        Type:=xlTypePDF, _
        Filename:=CStr(exportPath), _
        Quality:=xlQualityStandard, _
        IncludeDocProperties:=True, _
        IgnorePrintAreas:=False, _
        OpenAfterPublish:=False
    Exit Sub

HandleError:
    MsgBox "The Overview export could not be completed: " & Err.Description, _
        vbExclamation, "FP&A report export"
End Sub
