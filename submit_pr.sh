#!/bin/bash
# PR 提交脚本 - SuperPod 白皮书 OCS 拓扑认知方法

echo "=========================================="
echo "SuperPod 白皮书 PR 提交脚本"
echo "=========================================="
echo ""

# 配置变量
GITHUB_USERNAME="rockysonsun"  # GitHub 用户名
REPO_NAME="superpod-whitepaper"
BRANCH_NAME="add-ocs-topology-cognitive-method"

echo "步骤 1: Fork 仓库"
echo "请访问 https://github.com/DeepLink-org/superpod-whitepaper"
echo "点击右上角的 Fork 按钮"
echo ""
read -p "Fork 完成后按回车继续..."

echo ""
echo "步骤 2: 克隆 Fork 的仓库"
git clone https://github.com/${GITHUB_USERNAME}/${REPO_NAME}.git
cd ${REPO_NAME}

echo ""
echo "步骤 3: 创建新分支"
git checkout -b ${BRANCH_NAME}

echo ""
echo "步骤 4: 添加文章文件"
# 检查 src 目录是否存在
if [ -d "src" ]; then
    cp ~/superpod-ocs-topology-cognitive.md src/ocs-topology-cognitive-method.md
    echo "文件已复制到 src/ocs-topology-cognitive-method.md"
else
    cp ~/superpod-ocs-topology-cognitive.md ./ocs-topology-cognitive-method.md
    echo "文件已复制到 ocs-topology-cognitive-method.md"
fi

echo ""
echo "步骤 5: 提交更改"
git add .
git commit -m "Add OCS topology cognitive method based on optical module coding

- Introduce topology feature code pre-storage mechanism
- Describe automatic topology perception workflow  
- Provide three-stage development roadmap (perception-correction-upgrade)
- Include industry development suggestions balancing technology and commercialization

Related patent: 20260052-P26BJ0080CNCN"

echo ""
echo "步骤 6: 推送到 GitHub"
git push origin ${BRANCH_NAME}

echo ""
echo "=========================================="
echo "步骤 7: 创建 Pull Request"
echo "=========================================="
echo ""
echo "请访问: https://github.com/${GITHUB_USERNAME}/${REPO_NAME}"
echo "点击 'Compare & pull request' 按钮"
echo ""
echo "PR 标题:"
echo "Add OCS topology cognitive method based on optical module coding"
echo ""
echo "PR 描述:"
cat << 'EOF'
## 摘要
本文提出了一种基于光模块写码的OCS光传输拓扑认知与动态调整方法，通过预存拓扑特征码实现OCS对网络拓扑的自动感知和智能调度。

## 主要内容
- **拓扑特征码设计**：定义了包含设备标识、端口标识、OCS关联端口、对端连接信息、模块状态标识的完整字段结构
- **三阶段工作流程**：初始化阶段、运行监测阶段、业务调度阶段的详细流程
- **产业发展建议**：提出拓扑感知→拓扑修正→拓扑升级的三阶段发展路径
- **技术与商业平衡**：探讨如何在技术理想与商业现实之间找到平衡点

## 与白皮书的关系
SuperPod白皮书从架构层面探讨了超节点互联的拓扑方案（Dragonfly+OCS、3D Torus+OCS、大环路+dOCS），本文从实现层面提供具体的拓扑认知与动态调整机制，共同为产业发展提供从架构到落地的完整技术路径。

## 关联专利
- 专利号：20260052-P26BJ0080CNCN
- 专利名称：一种基于两端光模块写码的OCS光传输拓扑快速认知与动态调整方法及系统

---
**作者**：Rocky  
**日期**：2026-04-05
EOF

echo ""
echo "=========================================="
echo "完成！"
echo "=========================================="
