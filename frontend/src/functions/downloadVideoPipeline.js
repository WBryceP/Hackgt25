import { useState } from "react";

const useDownloadVideo = () => {
  const [loading, setLoading] = useState(false);
  const [downloadError, setDownloadError] = useState("");
  const [downloadVideoResult, setDownloadVideoResult] = useState(null);

  const downloadVideo = async (url) => {
    const re =
      /(^(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:watch\?(?:.*&)?v=|embed\/|v\/|shorts\/)|youtu\.be\/)([A-Za-z0-9_-]{11})(?=[^A-Za-z0-9_-]|$))/i;
    const id = url.match(re)?.[2];
    if (!id) {
      return;
    }

    try {
      setLoading(true);
      console.log(url);
      let res = await fetch(import.meta.env.VITE_BACKEND_URL + "/download", {
        method: "POST",
        body: JSON.stringify({
          url: url,
          format: "mp4",
          quality: 720,
        }),
      });

      let data = await res.json();
      if (data?.status !== "ok") {
        throw new Error("Error: status is not ok on downlod");
      }
      const jobId = data.jobId;
      if (!jobId) {
        throw new Error("Error: jobId is invalid");
      }
      url = new URL(import.meta.env.VITE_BACKEND_URL + "/status/" + jobId);

      res = await fetch(url);
      data = await res.json();
      if (data?.status !== "ok") {
        throw new Error("Error: status is not ok on checking jobId");
      }
      if (data?.data?.status !== "completed") {
        throw new Error("Error: download is not complete");
      }

      const fileName = data?.data?.fileName;
      if (!fileName) {
        throw new Error("Error: fileName is invalid");
      }

      url = new URL(
        import.meta.env.VITE_BACKEND_URL +
          "/downloadFile/" +
          jobId +
          "/" +
          fileName
      );
      res = await fetch(url);
      data = await res.json();
      setDownloadVideoResult(data);
    } catch (error) {
      setDownloadError("Error while downloading video: " + error);
      return;
    } finally {
      setLoading(false);
      setDownloadVideoResult(null);
    }
  };

  return [downloadVideo, downloadVideoResult, downloadError, loading];
};

export default useDownloadVideo;
