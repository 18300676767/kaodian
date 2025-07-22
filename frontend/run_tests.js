#!/usr/bin/env node
/**
 * 前端测试运行脚本
 * 支持运行所有测试、特定测试、生成覆盖率报告等
 */

const { spawn } = require('child_process');
const path = require('path');

function runCommand(command, args, description) {
  return new Promise((resolve, reject) => {
    console.log(`\n${'='.repeat(50)}`);
    console.log(`🚀 ${description}`);
    console.log(`${'='.repeat(50)}`);
    
    const child = spawn(command, args, {
      stdio: 'inherit',
      shell: true
    });
    
    child.on('close', (code) => {
      if (code === 0) {
        console.log('\n✅ 执行成功!');
        resolve();
      } else {
        console.log(`\n❌ 执行失败，退出代码: ${code}`);
        reject(new Error(`命令执行失败，退出代码: ${code}`));
      }
    });
    
    child.on('error', (error) => {
      console.log(`\n❌ 执行错误: ${error.message}`);
      reject(error);
    });
  });
}

async function main() {
  console.log('🧪 高考考点分析系统 - 前端测试套件');
  console.log('='.repeat(50));
  
  // 检查是否在正确的目录
  const packageJsonPath = path.join(process.cwd(), 'package.json');
  try {
    require(packageJsonPath);
  } catch (error) {
    console.log('❌ 错误: 请在frontend目录下运行此脚本');
    process.exit(1);
  }
  
  // 显示测试选项
  console.log('\n📋 可用测试选项:');
  console.log('1. 运行所有测试 (交互模式)');
  console.log('2. 运行所有测试 (一次性)');
  console.log('3. 生成覆盖率报告');
  console.log('4. 运行特定测试文件');
  console.log('5. 运行组件测试');
  console.log('6. 运行API服务测试');
  console.log('0. 退出');
  
  const readline = require('readline');
  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
  });
  
  const question = (query) => new Promise((resolve) => rl.question(query, resolve));
  
  while (true) {
    try {
      const choice = await question('\n请选择测试选项 (0-6): ');
      
      switch (choice.trim()) {
        case '0':
          console.log('👋 退出测试');
          rl.close();
          return;
          
        case '1':
          await runCommand('npm', ['test'], '运行所有测试 (交互模式)');
          break;
          
        case '2':
          await runCommand('npm', ['test', '--', '--watchAll=false'], '运行所有测试 (一次性)');
          break;
          
        case '3':
          await runCommand('npm', ['run', 'test:coverage'], '生成覆盖率报告');
          console.log('\n📊 覆盖率报告已生成在 coverage/ 目录');
          break;
          
        case '4':
          const testFile = await question('请输入测试文件名 (例如: Login.test.tsx): ');
          if (testFile.trim()) {
            await runCommand('npm', ['test', '--', '--testPathPattern', testFile.trim()], `运行测试文件 ${testFile.trim()}`);
          } else {
            console.log('❌ 文件名不能为空');
          }
          break;
          
        case '5':
          await runCommand('npm', ['test', '--', '--testPathPattern', 'components'], '运行组件测试');
          break;
          
        case '6':
          await runCommand('npm', ['test', '--', '--testPathPattern', 'services'], '运行API服务测试');
          break;
          
        default:
          console.log('❌ 无效选择，请输入 0-6');
          continue;
      }
      
      // 询问是否继续
      const continueTest = await question('\n是否继续运行其他测试? (y/n): ');
      if (continueTest.trim().toLowerCase() !== 'y') {
        break;
      }
      
    } catch (error) {
      console.log(`\n❌ 发生错误: ${error.message}`);
      break;
    }
  }
  
  rl.close();
}

// 处理中断信号
process.on('SIGINT', () => {
  console.log('\n\n👋 用户中断，退出测试');
  process.exit(0);
});

if (require.main === module) {
  main().catch((error) => {
    console.error(`\n💥 测试运行失败: ${error.message}`);
    process.exit(1);
  });
} 