

const download_file = async (downloadUrl: string, filename: string) => {
    try {
        const response = await fetch(downloadUrl);

        if (!response.ok) {
            throw new Error(`HTTP Error: ${response.status}`);
        }
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);

        const link = document.createElement("a");
        link.href = url;
        link.download = filename || "download";
        document.body.appendChild(link);
        link.click();

        document.body.removeChild(link);
        window.URL.revokeObjectURL(url);

        return true;
    } catch (error) {
        console.error("download failed", error);
    }
}

export default download_file;