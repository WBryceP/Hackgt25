This guide shows how you can use the Analyze API to generate summaries, chapters, and highlights from videos using pre-defined formats and optional prompts for customization.
- ** Summaries ** are concise overviews capturing the key points, adaptable into formats like paragraphs, emails, or bullet points based on your prompt.
- ** Chapters ** offer a chronological breakdown of the video, with timestamps, headlines, and summaries for each section.
- ** Highlights ** list the most significant events chronologically, including timestamps and brief descriptions.

Below are some examples of how to guide the platform in generating content tailored to your needs.

| Content type | Prompt example |
| : -------------------------- | : ----------------------------------------------------------------------------------------------------- |
| Specify the target audience | Generate a summary suitable for a high school audience studying environmental science.                 |
| Adjust the tone | Generate a light - hearted and humorous chapter breakdown of this documentary.                           |
| Indicate length constraints | Provide a summary fit for a Twitter post under 280 characters.                                         |
| Customize text format | Generate a summary in no more than 5 bullet points.                                                    |
| Specify the purpose | Summarize this video from a marketer's perspective, focusing on brand mentions and product placements. |

{/* This guide provides a complete example. For a simplified introduction with just the essentials, see the [Analyze videos](/v1.3/docs/get-started/quickstart/analyze-videos) quickstart guide. */ }

# Prerequisites

  - To use the platform, you need an API key:
<Steps>
  <Step>
    If you don’t have an account, [sign up](https://playground.twelvelabs.io/) for a free account.
  </Step>
  <Step>
    Go to the [API Key](https://playground.twelvelabs.io/dashboard/api-key) page.
  </Step>
  <Step>
    Select the **Copy** icon next to your key.
  </Step>
</Steps>
  - Ensure the TwelveLabs SDK is installed on your computer:

<CodeBlocks>
  ```shell Python
  pip install twelvelabs
  ```
  ```shell Node.js
  yarn add twelvelabs-js # or npm install twelvelabs-js
  ```
</CodeBlocks>

  - The videos you wish to use must meet the following requirements:
    - ** Video resolution **: Must be at least 360x360 and must not exceed 3840x2160.
    - ** Aspect ratio **: Must be one of 1: 1, 4: 3, 4: 5, 5: 4, 16: 9, 9: 16, or 17: 9.

  - ** Video and audio formats **: Your video files must be encoded in the video and audio formats listed on the < a href = "https://ffmpeg.org/ffmpeg-formats.html" target = "_blank" > FFmpeg Formats Documentation</a > page.For videos in other formats, contact us at[support@twelvelabs.io](mailto: support@twelvelabs.io).
    - ** Duration **: Must be between 4 seconds and 60 minutes(3600s).In a future release, the maximum duration will be 2 hours(7, 200 seconds).
    - ** File size **:  Must not exceed 2 GB.
     If you require different options, contact us at[support@twelvelabs.io](mailto: support@twelvelabs.io).

# Complete example

This complete example shows how to create an index, upload a video, and analyze videos to generate summaries, chapters, and highlights.Ensure you replace the placeholders surrounded by `<>` with your values.

< CodeBlocks >
  ```Python Python maxLines=8
    from twelvelabs import TwelveLabs
    from twelvelabs.indexes import IndexesCreateRequestModelsItem
    from twelvelabs.tasks import TasksRetrieveResponse

    # 1. Initialize the client
    client = TwelveLabs(api_key="<YOUR_API_KEY>")

    # 2. Create an index
    index = client.indexes.create(
        index_name="<YOUR_INDEX_NAME>",
        models=[
            IndexesCreateRequestModelsItem(
                model_name="pegasus1.2", model_options=["visual", "audio"]
            )
        ]
    )
    print(f"Created index: id={index.id}")

    # 3. Upload a video
    task = client.tasks.create(
        index_id=index.id, video_url="<YOUR_VIDEO_URL>")
    print(f"Created task: id={task.id}")

    # 4. Monitor the indexing process
    def on_task_update(task: TasksRetrieveResponse):
        print(f"  Status={task.status}")

    task = client.tasks.wait_for_done(sleep_interval= 5, task_id=task.id, callback=on_task_update)
    if task.status != "ready":
        raise RuntimeError(f"Indexing failed with status {task.status}")
    print(
        f"Upload complete. The unique identifier of your video is {task.video_id}.")

    # 5. Generate summaries, chapters, and highlights
    res_summary = client.summarize(
        video_id=task.video_id,
        type="summary",
        # prompt="<YOUR_PROMPT>",
        # temperature= 0.2
    )
    res_chapters = client.summarize(
        video_id=task.video_id,
        type="chapter",
        # prompt="<YOUR_PROMPT>",
        # temperature= 0.2
    )
    res_highlights = client.summarize(
        video_id=task.video_id,
        type="highlight",
        # prompt="<YOUR_PROMPT>",
        # temperature= 0.2
    )

    #6. Process the results
    print(f"Summary: {res_summary.summary}")
    for chapter in res_chapters.chapters:
        print(
            f"""Chapter {chapter.chapter_number},
    start={chapter.start_sec},
    end={chapter.end_sec}
    Title: {chapter.chapter_title}
    Summary: {chapter.chapter_summary}
    """
        )
    for highlight in res_highlights.highlights:
        print(
            f"Highlight: {highlight.highlight}, start: {highlight.start_sec}, end: {highlight.end_sec}")
    ```

    ```JavaScript Node.js maxLines=8
    import { TwelveLabs, TwelvelabsApi } from "twelvelabs-js";

    // 1. Initialize the client
    const client = new TwelveLabs({ apiKey: "<YOUR_API_KEY>" });

    // 2. Create an index
    const index = await client.indexes.create({
      indexName: "<YOUR_INDEX_NAME>",
      models: [
        {
          modelName: "pegasus1.2",
          modelOptions: ["visual", "audio"],
        },
      ],
    });
    console.log(`Created index: id = ${ index.id } `);

    // 3. Upload a video
    const createTaskResponse = await client.tasks.create({
      indexId: index.id!,
      videoUrl: "<YOUR_VIDEO_URL>",
    });
    console.log(`Created task: id = ${ createTaskResponse.id } `);

    // 4. Monitor the indexing process
    const task = await client.tasks.waitForDone(createTaskResponse.id!, {
        sleepInterval: 5,
        callback: (task: TwelvelabsApi.TasksRetrieveResponse) => {
            console.log(`  Status = ${ task.status } `);
        },
    });
    if (task.status !== "ready") {
      throw new Error(`Indexing failed with status ${ task.status } `);
    }
    console.log(
      `Upload complete.The unique identifier of your video is ${ task.videoId } `,
    );

    // 5. Generate summaries, chapters, and highlights
    const summary_res = await client.summarize({
      videoId: task.videoId!,
      type: "summary",
      // prompt: "<YOUR_PROMPT>",
      // temperature: 0.2
    });
    const chapters_res = await client.summarize({
      videoId: task.videoId!,
      type: "chapter",
      // prompt: "<YOUR_PROMPT>",
      // temperature: 0.2
    });
    const highlights_res = await client.summarize({
      videoId: task.videoId!,
      type: "highlight",
      // prompt: "<YOUR_PROMPT>",
      // temperature: 0.2
    });

    // 6. Process the results
    if ("summary" in summary_res) {
      console.log(`Summary: ${ summary_res.summary } `);
    }
    if ("chapters" in chapters_res && Array.isArray(chapters_res.chapters)) {
      const chapters = chapters_res.chapters;

      for (const chapter of chapters) {
        console.log(
          `Chapter ${ chapter.chapterNumber } \nstart = ${ chapter.startSec } \nend = ${ chapter.endSec } \nTitle = ${ chapter.chapterTitle } \nSummary = ${ chapter.chapterSummary } `,
        );
      }
    }
    if (
      "highlights" in highlights_res &&
      Array.isArray(highlights_res.highlights)
    ) {
      for (const highlight of highlights_res.highlights) {
        console.log(
          `Highlight: ${ highlight.highlight }, start: ${ highlight.startSec }, end: ${ highlight.endSec } `,
        );
      }
    }
    ```

</CodeBlocks >

# Step - by - step guide

  < Tabs >
  <Tab title="Python">
    <Steps>
      <Step title="Import the SDK and initialize the client">
          Create a client instance to interact with the TwelveLabs Video Understanding Platform.<br/>
          **Function call**: You call the [constructor](/v1.3/sdk-reference/python/the-twelve-labs-class#the-initializer) of the `TwelveLabs` class.<br/>
          **Parameters**:
          - `api_key`: The API key to authenticate your requests to the platform.<br/>

          **Return value**: An object of type `TwelveLabs` configured for making API calls.
      </Step>

      <Step title="Create an index">
          Indexes store and organize your video data, allowing you to group related videos. Create one before uploading videos.<br/>
          **Function call**: You call the [`indexes.create`](/v1.3/sdk-reference/python/manage-indexes#create-an-index) function.<br/><br/>
          **Parameters**:
          - `index_name`: The name of the index.
          - `models`: An array specifying your model configuration.

          See the [Indexes](/v1.3/docs/concepts/indexes) page for more details on creating an index and specifying the model configuration.<br/>

          **Return value**: An object containing, among other information, a field named `id` representing the unique identifier of the newly created index.
      </Step>
      <Step title="Upload videos">
          To perform any downstream tasks, you must first upload your videos, and the platform must finish indexing them.<br/>
          **Function call**: You call the [`tasks.create`](/v1.3/sdk-reference/python/upload-videos#create-a-video-indexing-task) function.<br/>
          **Parameters**:
          - `index_id`: The unique identifier of your index.
          - `video_url` or `video_file`: The publicly accessible URL or the path of your video file.<br/>

          **Return value**: An object of type `TasksCreateResponse` that you can use to track the status of your video upload and indexing process. This object contains, among other information, the following fields:
          - `id`: The unique identifier of your video indexing task.
          - `video_id`: The unique identifier of your video.
          <Note title="Note">
              You can also upload multiple videos in a single API call. For details, see the [Cloud-to-cloud integrations](/v1.3/docs/advanced/cloud-to-cloud-integrations) page.
          </Note>
      </Step>

      <Step title="Monitor the indexing process">
          The platform requires some time to index videos. Check the status of the video indexing task until it's completed.<br/>
          **Function call**: You call the [`tasks.wait_for_done`](/v1.3/sdk-reference/python/upload-videos#wait-for-a-video-indexing-task-to-complete) function.<br/>
          **Parameters**:
          - `sleep_interval`: The time interval, in seconds, between successive status checks. In this example, the method checks the status every five seconds.
          - `task_id`: The unique identifier of your video indexing task.
          - `callback`:  A callback function that the SDK executes each time it checks the status.<br/>

          **Return value**: An object of type `TasksRetrieveResponse` containing, among other information, a field named `status` representing the status of your task. Wait until the value of this field is `ready`.
      </Step>
      <Step title="Generate summaries, chapters, and highlights">
        **Function call**: You call the [`summarize`](/v1.3/sdk-reference/python/analyze-videos#summaries-chapters-and-highlights) method.<br/>
        **Parameters**:
        - `video_id`: The unique identifier of the video for which you want to generate text.
        - `type`: The type of text you want to generate. It can take one of the following values: "summary", "chapter", or "highlight".
        - _(Optional)_ `prompt`: A string you can use to provide context for the summarization task. The maximum length of a prompt is 2,000 tokens. Example: "Generate chapters using casual and conversational language to match the vlogging style of the video."
        - _(Optional)_  `temperature`: A number that controls the randomness of the text. A higher value generates more creative text, while a lower value produces more deterministic text.<br/>

        **Return value**: An object containing the generated content. The response type varies based on the `type` parameter:
        - When `type` is `summary`: Returns a `Summary` object with an id, `summary` text, and `usage` information
        - When `type` is `chapter`: Returns a `Chapter` object with an `id`, array of `chapters`, and `usage` information
        - When type is `highlight`: Returns a `Highlight` object with an `id`, array of `highlights`, and `usage` information
      </Step>
      <Step title="Process the results">
        For summaries, you can directly print the result. You must iterate over the list and print each item individually for chapters, and highlights.
      </Step>
    </Steps>
  </Tab>
  <Tab title="Node.js">
    <Steps>
      <Step title="Import the SDK and initialize the client">
          Create a client instance to interact with the TwelveLabs Video Understanding Platform.<br/>
          **Function call**: You call the [constructor](/v1.3/sdk-reference/node-js/the-twelve-labs-class#the-constructor) of the `TwelveLabs` class.<br/>
          **Parameters**:
          - `apiKey`: The API key to authenticate your requests to the platform.<br/>

          **Return value**: An object of type `TwelveLabs` configured for making API calls.
      </Step>

      <Step title="Create an index">
          Indexes store and organize your video data, allowing you to group related videos. Create one before uploading videos.<br/>
          **Function call**: You call the [`indexes.create`](/v1.3/sdk-reference/node-js/manage-indexes#create-an-index) function.<br/>
          **Parameters**:
          - `indexName`: The name of the index.
          - `models`: An array specifying your model configuration.

          See the [Indexes](/v1.3/docs/concepts/indexes) page for more details on creating an index and specifying the model configuration.<br/>

          **Return value**: An object containing, among other information, a field named `id` representing the unique identifier of the newly created index.
      </Step>
      <Step title="Upload videos">
          To perform any downstream tasks, you must first upload your videos, and the platform must finish indexing them.<br/>
          **Function call**: You call the [`tasks.create`](/v1.3/sdk-reference/node-js/upload-videos#create-a-video-indexing-task) function.<br/>
          **Parameters**:
          - `indexId`: The unique identifier of your index.
          - `videoUrl` or `videoFile`: The publicly accessible URL or the path of your video file.<br/>

          **Return value**: An object of type `TasksCreateResponse` that you can use to track the status of your video upload and indexing process. This object contains, among other information, the following fields:
          - `id`: The unique identifier of your video indexing task.
          - `videoId`: The unique identifier of your video.
          <Note title="Note">
              You can also upload multiple videos in a single API call. For details, see the [Cloud-to-cloud integrations](/v1.3/docs/advanced/cloud-to-cloud-integrations) page.
          </Note>
      </Step>
      <Step title="Monitor the indexing process">
          The platform requires some time to index videos. Check the status of the video indexing task until it's completed.<br/>
          **Function call**: You call the [`tasks.waitForDone`](/v1.3/sdk-reference/node-js/upload-videos#wait-for-a-video-indexing-task-to-complete) function.<br/>
          **Parameters**:
          - `sleepInterval`: The time interval, in seconds, between successive status checks. In this example, the method checks the status every five seconds.
          - `taskId`: The unique identifier of your video indexing task.
          - `callback`:  A callback function that the SDK executes each time it checks the status.<br/>

          **Return value**: An object of type `TasksRetrieveResponse` containing, among other information, a field named `status` representing the status of your task. Wait until the value of this field is `ready`.
      </Step>
      <Step title="Generate summaries, chapters, and highlights">
        **Function call**: You call the [`summarize`](/v1.3/sdk-reference/node-js/analyze-videos#summaries-chapters-and-highlights) method.<br/>
        **Parameters**:
        - `video_id`: The unique identifier of the video for which you want to generate text.
        - `type`: Type of text you want to generate. It can take one of the following values: "summary", "chapter", or "highlight".
        - _(Optional)_ `prompt`: A string you can use to provide context for the summarization task. The maximum length of a prompt is 2,000 tokens. Example: "Generate chapters using casual and conversational language to match the vlogging style of the video."
        - _(Optional)_  `temperature`: A number that controls the randomness of the text. A higher value generates more creative text, while a lower value produces more deterministic text.<br/>

        **Return value**: An object containing the generated content. The response type varies based on the `type` parameter:
        - When `type` is `summary`: Returns a `Summary` object with an id, `summary` text, and `usage` information
        - When `type` is `chapter`: Returns a `Chapter` object with an `id`, array of `chapters`, and `usage` information
        - When type is `highlight`: Returns a `Highlight` object with an `id`, array of `highlights`, and `usage` information
      </Step>
      <Step title="Process the results">
        For summaries, you can directly print the result. You must iterate over the list and print each item individually for chapters, and highlights.
      </Step>
    </Steps>
  </Tab>
</Tabs >
