/**
 * @template R
 * @callback Parser
 * @param {string[]} rows
 * @return {R | undefined}
 */

/**
 * @template O
 * @typedef {{[key: string]: keyof O}} HeadersFor
 */

/** Creates a parser that recognises a table with headings
 * @template T
 * @param {HeadersFor<T>} headers the table heading regexes and their corresponding keys
 * @return {Parser<T>} the relevant parser
 */
export function table_parser(headers) {
    return function (text_rows) {
        const rows = text_rows
            .flatMap(row => row.split('\n\n'))
            .filter(row => row !== '')

        const entries = rows.flatMap(row =>
            Object.entries(headers).flatMap(([header, key]) => {
                // const match = row.match(RegExp(`^\\s*(?:${header})\\s*(.*)`, 'si'))
                const match = row.match(RegExp(`(?:${header})\\s*(.*)`, 'si'))
                if (!match && key === "date_of_report") {
                    const date_match = row.match(/\b(?:\d{1,2}[-/]\d{1,2}[-/]\d{2,4}|\d{1,2}\s(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)[ ,.-]\s?\d{2,4}|\d{2,4}[-/]\d{1,2}[-/]\d{1,2})\b/g);
                    if (date_match) {
                        return [[key, date_match[0]]]
                    }
                }
                return match ? [[key, match[1]]] : []
                }
            )
        )
        const uniqueArray = entries.filter((el, index, self) =>
                index === self.findIndex((t) => (
                    t[0] === el[0]
                ))
        );
        return Object.fromEntries(uniqueArray)
    }
}
