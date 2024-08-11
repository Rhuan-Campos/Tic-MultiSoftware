//  funções para buscar dados do servidor
export async function fetchColumns() {
    const response = await fetch('/get-columns');
    if (!response.ok) {
        throw new Error('Erro ao buscar colunas');
    }
    const data = await response.json();
    return data.columns;
}

export async function fetchUniqueCounts(column) {
    const response = await fetch(`/get-unique-counts?column=${encodeURIComponent(column)}`);
    if (!response.ok) {
        throw new Error('Erro ao buscar contagens únicas');
    }
    const data = await response.json();
    return data;
}
