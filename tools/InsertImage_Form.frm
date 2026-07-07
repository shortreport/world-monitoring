VERSION 5.00
Begin {C62A69F0-16DC-11CE-9E98-00AA00574A4F} frmInsertImage
   Caption         =   "画像を選んで貼り付け"
   ClientHeight    =   5640
   ClientLeft      =   120
   ClientTop       =   465
   ClientWidth     =   5160
   OleObjectBlob   =   "frmInsertImage.frx":0000
   StartUpPosition =   1  'オーナーの中央
End
Attribute VB_Name = "frmInsertImage"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = False

' ============================================================
' フォームの初期化
' ============================================================
Private Sub UserForm_Initialize()
    ' ラベル設定
    Me.Caption = "画像を選んで貼り付け"

    ' ラジオボタンのラベルをモジュールの定数から取得
    opt1.Caption = IMG_LABEL_1
    opt2.Caption = IMG_LABEL_2
    opt3.Caption = IMG_LABEL_3
    opt1.Value = True  ' デフォルト選択

    ' デフォルト値をテキストボックスに設定
    txtLeft.Text = CStr(DEFAULT_LEFT)
    txtTop.Text = CStr(DEFAULT_TOP)
    txtWidth.Text = CStr(DEFAULT_WIDTH)
    txtHeight.Text = CStr(DEFAULT_HEIGHT)
End Sub

' ============================================================
' 貼り付けボタン
' ============================================================
Private Sub btnInsert_Click()
    Dim imagePath As String
    Dim leftCm As Double, topCm As Double
    Dim widthCm As Double, heightCm As Double

    ' 画像パスの選択
    If opt1.Value Then
        imagePath = IMG_PATH_1
    ElseIf opt2.Value Then
        imagePath = IMG_PATH_2
    ElseIf opt3.Value Then
        imagePath = IMG_PATH_3
    End If

    ' 入力値の検証と取得
    On Error GoTo InputError
    leftCm = CDbl(txtLeft.Text)
    topCm = CDbl(txtTop.Text)
    widthCm = CDbl(txtWidth.Text)
    heightCm = CDbl(txtHeight.Text)
    On Error GoTo 0

    ' 値の範囲チェック
    If widthCm <= 0 Or heightCm <= 0 Then
        MsgBox "幅・高さは0より大きい値を入力してください。", vbExclamation
        Exit Sub
    End If

    ' 挿入実行
    Me.Hide
    InsertImageToDoc imagePath, leftCm, topCm, widthCm, heightCm
    Unload Me
    Exit Sub

InputError:
    MsgBox "数値を正しく入力してください（例: 1.5）", vbExclamation
End Sub

' ============================================================
' キャンセルボタン
' ============================================================
Private Sub btnCancel_Click()
    Unload Me
End Sub
