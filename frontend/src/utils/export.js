function quote(value) {
  const text = value == null ? '' : String(value)
  return `"${text.replaceAll('"', '""')}"`
}

export function downloadCsv(filename, columns, rows) {
  const content = [
    columns.map(column => quote(column.title)).join(','),
    ...rows.map(row => columns.map(column => quote(row[column.dataIndex])).join(',')),
  ].join('\n')
  const blob = new Blob([`\uFEFF${content}`], { type: 'text/csv;charset=utf-8' })
  const url = URL.createObjectURL(blob)
  const link = document.createElement('a')
  link.href = url
  link.download = filename
  link.click()
  URL.revokeObjectURL(url)
}
