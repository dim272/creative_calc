function addRow() {
  const div = document.createElement('div');
  div.className = 'creator_material';
  div.innerHTML = `
        <input type="text" name="m_name" placeholder="Название материала" />
        <input type="text" name="m_quantity" placeholder="Необходимое количество" />
        <input type="text" name="m_total_quantity" placeholder="Количество в упаковке" />
        <input type="text" name="m_price" placeholder="Стоимость упаковки" />
        <input type="button" value="Удалить" onclick="removeRow(this)" />
  `;
  document.getElementById('materials').appendChild(div);
}

function removeRow(input) {
  document.getElementById('materials').removeChild(input.parentNode);
}