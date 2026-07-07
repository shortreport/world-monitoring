Attribute VB_Name = "InsertImageModule"
' ============================================================
' 画像貼り付けマクロ - メインモジュール
' 使い方: マクロ「InsertImageMain」を実行
' ============================================================

' ★ 画像パスをここに設定してください ★
Public Const IMG_PATH_1 As String = "C:\画像フォルダ\画像1.png"
Public Const IMG_PATH_2 As String = "C:\画像フォルダ\画像2.png"
Public Const IMG_PATH_3 As String = "C:\画像フォルダ\画像3.png"

' ★ ラベル名（フォームに表示される名前）
Public Const IMG_LABEL_1 As String = "画像1"
Public Const IMG_LABEL_2 As String = "画像2"
Public Const IMG_LABEL_3 As String = "画像3"

' ★ デフォルト位置・サイズ（単位: cm）
Public Const DEFAULT_LEFT As Double = 1.5    ' 左端からの距離
Public Const DEFAULT_TOP As Double = 2.0     ' 上端からの距離
Public Const DEFAULT_WIDTH As Double = 6.0   ' 幅
Public Const DEFAULT_HEIGHT As Double = 4.5  ' 高さ

' ============================================================
' メイン処理：フォームを表示
' ============================================================
Sub InsertImageMain()
    frmInsertImage.Show
End Sub

' ============================================================
' 画像をドキュメントに挿入する処理
' ============================================================
Sub InsertImageToDoc(imagePath As String, _
                     leftCm As Double, topCm As Double, _
                     widthCm As Double, heightCm As Double)

    Dim doc As Document
    Dim shp As Shape
    Dim cmToPt As Double
    cmToPt = 28.3464566929134  ' 1cm = 28.35pt

    ' ファイル存在チェック
    If Dir(imagePath) = "" Then
        MsgBox "画像ファイルが見つかりません:" & vbCrLf & imagePath, vbExclamation, "エラー"
        Exit Sub
    End If

    Set doc = ActiveDocument

    ' 浮動オブジェクトとして挿入（手動で移動・リサイズ可能）
    Set shp = doc.Shapes.AddPicture( _
        FileName:=imagePath, _
        LinkToFile:=False, _
        SaveWithDocument:=True, _
        Left:=leftCm * cmToPt, _
        Top:=topCm * cmToPt, _
        Width:=widthCm * cmToPt, _
        Height:=heightCm * cmToPt)

    ' 位置基準をページに設定（ページ左上を原点にする）
    With shp
        .RelativeHorizontalPosition = wdRelativeHorizontalPositionPage
        .RelativeVerticalPosition = wdRelativeVerticalPositionPage
        .Left = leftCm * cmToPt
        .Top = topCm * cmToPt
        .WrapFormat.Type = wdWrapInFront  ' 前面配置
    End With

    MsgBox "画像を貼り付けました。" & vbCrLf & _
           "Word上で位置・サイズを自由に調整できます。", vbInformation, "完了"
End Sub
