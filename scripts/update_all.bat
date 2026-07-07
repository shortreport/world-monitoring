@echo off
REM ============================================================
REM update_all.bat
REM 手動で全コンテンツを強制更新したい場合にダブルクリックで実行
REM （GitHub Actions が使えない場合のローカル代替としても利用可）
REM ============================================================
cd /d "C:\Users\shondo\Desktop\agent_project"
call venv\Scripts\activate.bat

echo [%date% %time%] 全コンテンツ更新開始...

python trump_monitor.py
python generate_site.py

git add docs/
git diff --staged --quiet && (
    echo [%date% %time%] 変更なし。スキップ。
) || (
    git commit -m "Manual update: %date%"
    git push
    echo [%date% %time%] プッシュ完了。サイトに反映されます（約1〜2分）。
)

pause
