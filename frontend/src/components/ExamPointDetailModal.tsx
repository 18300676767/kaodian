import React from 'react';
import 'katex/dist/katex.min.css';
import { BlockMath, InlineMath } from 'react-katex';
import { ExamPoint } from '../config/examPointConfig';

interface Props {
  examPoint: ExamPoint | null;
  onClose: () => void;
  provinceList: {id:number, name:string}[];
}

// 自动补全公式反斜杠，并还原单斜杠为双斜杠
function autoFixLatex(desc: string) {
  // 先将所有单斜杠替换为双斜杠，防止后端/数据库转义丢失
  let fixed = desc.replace(/\\/g, '\\');
  // 替换常见latex关键字前加反斜杠（避免重复加）
  fixed = fixed
    .replace(/([^\\])frac/g, '$1\\frac')
    .replace(/([^\\])sqrt/g, '$1\\sqrt')
    .replace(/([^\\])leq/g, '$1\\leq')
    .replace(/([^\\])geq/g, '$1\\geq')
    .replace(/([^\\])sum/g, '$1\\sum')
    .replace(/([^\\])int/g, '$1\\int')
    .replace(/([^\\])log/g, '$1\\log')
    .replace(/([^\\])sin/g, '$1\\sin')
    .replace(/([^\\])cos/g, '$1\\cos')
    .replace(/([^\\])tan/g, '$1\\tan')
    .replace(/([^\\])cdot/g, '$1\\cdot')
    .replace(/([^\\])times/g, '$1\\times')
    .replace(/([^\\])div/g, '$1\\div')
    .replace(/([^\\])left/g, '$1\\left')
    .replace(/([^\\])right/g, '$1\\right');
  return fixed;
}

// 支持$...$行内和$$...$$块级公式混合渲染
function renderMixedDescription(desc: string) {
  // 先处理块级公式
  const blockParts = desc.split(/(\$\$[^$]+\$\$)/g);
  return (
    <div style={{ whiteSpace: 'pre-wrap' }}>
      {blockParts.map((block, i) => {
        if (block.startsWith('$$') && block.endsWith('$$')) {
          return <BlockMath key={i} math={block.slice(2, -2)} />;
        }
        // 按行处理，自动识别整行公式
        return block.split(/\n/).map((line, j) => {
          // 1. 整行公式自动识别（无中文，且只含公式常用字符）
          if (/^[A-Za-z0-9_\^\-\+\*\/\(\)\[\]\{\}=<>\|,. :;\\]+$/.test(line.trim()) && !/[\u4e00-\u9fa5]/.test(line)) {
            return line.trim() ? <BlockMath key={i + '-' + j} math={line.trim()} /> : <br key={i + '-' + j} />;
          }
          // 2. 行内$...$公式
          const inlineParts = line.split(/(\$[^$]+\$)/g);
          return inlineParts.map((part, k) =>
            part.startsWith('$') && part.endsWith('$') ? (
              <InlineMath key={i + '-' + j + '-' + k} math={part.slice(1, -1)} />
            ) : (
              <span key={i + '-' + j + '-' + k}>{part}</span>
            )
          );
        });
      })}
    </div>
  );
}

// 描述渲染函数
const renderDescription = (desc: string) => {
  return desc.split('\n').map((line, idx) => {
    const latexMatch = line.match(/^\$(.*)\$$/);
    if (latexMatch) {
      return <BlockMath key={idx} math={latexMatch[1]} />;
    }
    return <div key={idx}>{line}</div>;
  });
};

const ExamPointDetailModal: React.FC<Props> = ({ examPoint, onClose, provinceList }) => {
  if (!examPoint) return null;
  // 自动补全公式反斜杠
  const descFixed = autoFixLatex(examPoint.description);
  // 省份名称优先用 province_id 匹配，无则空字符串
  let provinceName = '';
  if (examPoint.province_id && provinceList && provinceList.length > 0) {
    const found = provinceList.find(p => p.id === examPoint.province_id);
    provinceName = found ? found.name : '';
  }
  // 调试输出
  console.log('原始description:', examPoint.description);
  console.log('修正后descFixed:', descFixed);

  return (
    <div className="fixed inset-0 bg-black bg-opacity-30 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg shadow-lg p-6 w-full max-w-lg relative">
        <h2 className="text-xl font-bold mb-4">考点详情</h2>
        <div className="mb-2"><b>省份：</b>{provinceName}</div>
        <div className="mb-2"><b>科目：</b>{examPoint.subject}</div>
        <div className="mb-2"><b>年级：</b>{examPoint.grade}</div>
        <div className="mb-2"><b>学期：</b>{examPoint.semester}</div>
        <div className="mb-2"><b>一级考点：</b>{examPoint.level1_point}</div>
        <div className="mb-2"><b>二级考点：</b>{examPoint.level2_point}</div>
        <div className="mb-2"><b>三级考点：</b>{examPoint.level3_point}</div>
        <div className="mb-2"><b>覆盖率：</b>{examPoint.coverage_rate}</div>
        <div className="mb-2"><b>描述：</b>{renderMixedDescription(descFixed)}</div>
        {/* 强制渲染一条BlockMath公式用于调试 */}
        <div className="mb-2"><b>公式调试：</b><BlockMath math={'f(x)=\\frac{1}{\\sqrt{x-2}}'} /></div>
        <button className="absolute top-2 right-2 text-gray-500 hover:text-gray-800" onClick={onClose}>关闭</button>
      </div>
    </div>
  );
};

export default ExamPointDetailModal; 