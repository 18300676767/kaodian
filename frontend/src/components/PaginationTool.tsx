import React, { useState } from "react";

interface PaginationToolProps {
  total: number;
  page: number;
  pageSize: number;
  onPageChange: (page: number) => void;
  onPageSizeChange: (size: number) => void;
  pageSizeOptions?: number[];
}

const PaginationTool: React.FC<PaginationToolProps> = ({
  total,
  page,
  pageSize,
  onPageChange,
  onPageSizeChange,
  pageSizeOptions = [10, 20, 50, 100],
}) => {
  const totalPages = Math.max(1, Math.ceil(total / pageSize));
  const [inputPage, setInputPage] = useState(page);

  React.useEffect(() => {
    setInputPage(page);
  }, [page]);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = Number(e.target.value);
    setInputPage(value);
  };

  const handleInputBlur = () => {
    if (inputPage >= 1 && inputPage <= totalPages) {
      onPageChange(inputPage);
    } else {
      setInputPage(page);
    }
  };

  return (
    <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
      <span>每页</span>
      <select
        value={pageSize}
        onChange={e => onPageSizeChange(Number(e.target.value))}
      >
        {pageSizeOptions.map(opt => (
          <option key={opt} value={opt}>{opt}</option>
        ))}
      </select>
      <span>条</span>
      <button disabled={page === 1} onClick={() => onPageChange(page - 1)}>上一页</button>
      <input
        type="number"
        min={1}
        max={totalPages}
        value={inputPage}
        onChange={handleInputChange}
        onBlur={handleInputBlur}
        style={{ width: 50 }}
      />
      <span>/ {totalPages} 页</span>
      <button disabled={page === totalPages} onClick={() => onPageChange(page + 1)}>下一页</button>
      <span>共 {total} 条</span>
    </div>
  );
};

export default PaginationTool; 