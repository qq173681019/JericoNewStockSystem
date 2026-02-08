#!/bin/bash

echo "=========================================="
echo "部署配置测试 / Deployment Configuration Test"
echo "=========================================="
echo ""

# 测试 1: 检查必需文件
echo "✓ 测试 1: 检查配置文件..."
files=("app.py" "vercel.json" "railway.json" "Procfile" "requirements-prod.txt" "Dockerfile")
for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        echo "  ✅ $file 存在"
    else
        echo "  ❌ $file 缺失"
        exit 1
    fi
done
echo ""

# 测试 2: 测试本地环境
echo "✓ 测试 2: 本地环境路径..."
result=$(python3 -c "from config.settings import DATA_DIR, IS_CLOUD_ENV; print(f'{IS_CLOUD_ENV}|{DATA_DIR}')" 2>&1)
is_cloud=$(echo $result | cut -d'|' -f1)
data_dir=$(echo $result | cut -d'|' -f2)
if [ "$is_cloud" = "False" ]; then
    echo "  ✅ 本地环境检测正确: IS_CLOUD_ENV=False"
    echo "  ✅ 数据目录: $data_dir"
else
    echo "  ❌ 本地环境检测失败"
    exit 1
fi
echo ""

# 测试 3: 测试云环境
echo "✓ 测试 3: 云环境路径..."
result=$(RAILWAY_PUBLIC_DOMAIN=test.railway.app python3 -c "from config.settings import DATA_DIR, IS_CLOUD_ENV; print(f'{IS_CLOUD_ENV}|{DATA_DIR}')" 2>&1)
is_cloud=$(echo $result | cut -d'|' -f1)
data_dir=$(echo $result | cut -d'|' -f2)
if [ "$is_cloud" = "True" ] && [ "$data_dir" = "/tmp/data" ]; then
    echo "  ✅ 云环境检测正确: IS_CLOUD_ENV=True"
    echo "  ✅ 数据目录: $data_dir"
else
    echo "  ❌ 云环境检测失败"
    exit 1
fi
echo ""

# 测试 4: 测试应用导入
echo "✓ 测试 4: Flask 应用导入..."
if python3 -c "from app import app; print('OK')" 2>&1 | grep -q "OK"; then
    echo "  ✅ Flask 应用导入成功"
else
    echo "  ❌ Flask 应用导入失败"
    exit 1
fi
echo ""

# 测试 5: 检查 Gunicorn
echo "✓ 测试 5: Gunicorn 安装..."
if python3 -c "import gunicorn; print('OK')" 2>&1 | grep -q "OK"; then
    echo "  ✅ Gunicorn 已安装"
else
    echo "  ❌ Gunicorn 未安装"
    exit 1
fi
echo ""

echo "=========================================="
echo "🎉 所有测试通过！部署配置正确！"
echo "🎉 All tests passed! Deployment config is correct!"
echo "=========================================="
echo ""
echo "下一步 / Next Steps:"
echo "1. 合并此 PR / Merge this PR"
echo "2. 部署到 Railway 或 Vercel / Deploy to Railway or Vercel"
echo "3. 查看文档 / Read documentation:"
echo "   - DEPLOYMENT_GUIDE.md (English)"
echo "   - 部署修复说明.md (中文)"
echo ""
