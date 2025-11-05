export async function deletePriceLabelsFile(file) {
    return await fetch(
        `/price-labes/files/delete/${file}`,
        {method: 'DELETE'}
    );
}
