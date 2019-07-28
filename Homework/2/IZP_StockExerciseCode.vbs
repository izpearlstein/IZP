Sub StockExercise()

'Go through all the sheets in the workbook
Dim ws As Worksheet
    For Each ws In ActiveWorkbook.Worksheets
    ws.Activate
        'Find the last row in each sheet
        LastRow = ws.Cells(Rows.Count, 1).End(xlUp).Row

        'Headers for summary table
        Cells(1, 9).Value = "Ticker"
        Cells(1, 10).Value = "Yearly Change"
        Cells(1, 11).Value = "Percent Change"
        Cells(1, 12).Value = "Total Volume"
        'Create variables
        Dim Opening_Price As Double
        Dim Closing_Price As Double
        Dim Yearly_Change As Double
        Dim Ticker_Name As String
        Dim Percent_Change As Double
        Dim Volume As Double
        'Start volume at zero for summation
        Volume = 0
        'Row and column variables for summation and summary table
        Dim Row As Double
        Row = 2
        Dim Column As Integer
        Column = 1
        Dim i As Long
        
        'Set first opening price
        Opening_Price = Cells(2, Column + 2).Value
         
         'Loop through all ticker symbols in first column
        For i = 2 To LastRow
         'Condition for ticker symbols not equal
            If Cells(i + 1, Column).Value <> Cells(i, Column).Value Then
                Ticker_Name = Cells(i, Column).Value
                Cells(Row, Column + 8).Value = Ticker_Name
                'Set closing price
                Closing_Price = Cells(i, Column + 5).Value
                'Set yearly change
                Yearly_Change = Closing_Price - Opening_Price
                Cells(Row, Column + 9).Value = Yearly_Change
                'Set percent change
                If (Opening_Price = 0 And Closing_Price = 0) Then
                    Percent_Change = 0
                ElseIf (Opening_Price = 0 And Closing_Price <> 0) Then
                    Percent_Change = 1
                Else
                    Percent_Change = Yearly_Change / Opening_Price
                    Cells(Row, Column + 10).Value = Percent_Change
                    Cells(Row, Column + 10).NumberFormat = "0.00%"
                End If
                'Set total volume
                Volume = Volume + Cells(i, Column + 6).Value
                Cells(Row, Column + 11).Value = Volume
                'Set summary table rows
                Row = Row + 1
                'Reset opening price for iteration
                Opening_Price = Cells(i + 1, Column + 2)
                'Reset total volume for iteration
                Volume = 0
            'Condition if ticker symbols are the same
            Else
                Volume = Volume + Cells(i, Column + 6).Value
            End If
        Next i
        
        'Find last row of summary table for each sheet
        sumLastRow = ws.Cells(Rows.Count, Column + 8).End(xlUp).Row
        'Format cells of summary table
        For j = 2 To sumLastRow
            If (Cells(j, Column + 9).Value > 0 Or Cells(j, Column + 9).Value = 0) Then
                Cells(j, Column + 9).Interior.ColorIndex = 10
            ElseIf Cells(j, Column + 9).Value < 0 Then
                Cells(j, Column + 9).Interior.ColorIndex = 3
            End If
        Next j
        
    Next ws
        
End Sub