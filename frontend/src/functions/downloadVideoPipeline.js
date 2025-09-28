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

      // POST /download
      let res = await fetch(import.meta.env.VITE_BACKEND_URL + "/download", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
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
      console.log(data);
      const jobId = data.jobId;
      if (!jobId) {
        throw new Error("Error: jobId is invalid");
      }
      url = new URL(import.meta.env.VITE_BACKEND_URL + "/status/" + jobId);

      // GET /status
      let fileName;

      while (true) {
        const res = await fetch(url);
        const data = await res.json();
        console.log(data);

        // Transport / API status
        if (data?.status !== "ok") {
          throw new Error("Error: status is not ok on checking jobId");
        }

        // Job status
        if (data?.data?.status === "completed") {
          console.log("Job completed!");
          fileName = data?.data?.filename;
          console.log(fileName);
          break;
        }

        await sleep(2500); // wait before next request
      }

      if (!fileName) {
        throw new Error("Error: fileName is invalid");
      }
      console.log(jobId);
      console.log(fileName);
      url = new URL(
        import.meta.env.VITE_BACKEND_URL +
          "/downloadFile/" +
          jobId +
          "/" +
          jobId +
          ".mp4"
      );
      console.log(url);

      // GET /downloadFile
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

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}
