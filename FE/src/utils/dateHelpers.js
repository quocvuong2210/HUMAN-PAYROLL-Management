/**
 * Convert any date format to YYYY-MM-DD for HTML input[type="date"]
 * Handles both ISO format and GMT string format
 * 
 * @param {string|Date} dateValue - Date in any format
 * @returns {string} Date in YYYY-MM-DD format or empty string
 * 
 * @example
 * formatDateForInput("2004-01-20T00:00:00.000Z") // "2004-01-20"
 * formatDateForInput("Tue, 20 Jan 2004 00:00:00 GMT") // "2004-01-20"
 * formatDateForInput(null) // ""
 */
export const formatDateForInput = (dateValue) => {
    if (!dateValue) return '';

    try {
        // Convert to Date object (handles both ISO and GMT formats)
        const date = new Date(dateValue);

        // Check if valid date
        if (isNaN(date.getTime())) {
            console.warn('Invalid date value:', dateValue);
            return '';
        }

        // Format to YYYY-MM-DD
        const year = date.getFullYear();
        const month = String(date.getMonth() + 1).padStart(2, '0');
        const day = String(date.getDate()).padStart(2, '0');

        return `${year}-${month}-${day}`;
    } catch (err) {
        console.error('Error formatting date:', err, dateValue);
        return '';
    }
};

/**
 * Format date for display (Vietnamese format)
 * 
 * @param {string|Date} dateValue - Date in any format
 * @returns {string} Date in DD/MM/YYYY format
 * 
 * @example
 * formatDateForDisplay("2004-01-20T00:00:00.000Z") // "20/01/2004"
 */
export const formatDateForDisplay = (dateValue) => {
    if (!dateValue) return 'Chưa cập nhật';

    try {
        const date = new Date(dateValue);
        if (isNaN(date.getTime())) return 'Chưa cập nhật';

        return date.toLocaleDateString('vi-VN');
    } catch (err) {
        console.error('Error formatting date for display:', err);
        return 'Chưa cập nhật';
    }
};
