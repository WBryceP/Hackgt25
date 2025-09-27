When analyzing video content to generate summaries or open-ended text, you can request structured JSON responses. This feature allows you to retrieve predictable, machine-readable outputs.

Key features:
- **Control response structure**: Define exactly how you want your video analysis results formatted using JSON schemas.
- **Process responses programmatically**: Eliminate manual parsing by receiving data in predictable, machine-readable formats.
- **Validate data automatically**: Ensure response fields meet your requirements with built-in type and format validation.
- **Stream structured content**: Get real-time JSON responses as analysis progresses without waiting for completion.
- **Integrate seamlessly**: Connect video analysis directly into your existing data pipelines and applications.

Use cases:
- **Directly populate data into databases**: Store video analysis results in structured tables without manual formatting.
- **Create automated reports**: Generate consistent video summaries and insights for business intelligence dashboards.
- **Build content recommendation systems**: Extract keywords and topics to power personalized content suggestions.
- **Populate content management systems**: Auto-generate video titles, descriptions, and tags in your CMS workflow.
- **Facilitate search and filtering**: Organize video metadata to make content discoverable across your platform

# Prerequisites

- You already know how to analyze videos and generate open-ended text and summaries based on the content of your videos. For instructions, see the [Open-ended analysis](/v1.3/docs/guides/analyze-videos/open-ended-analysis) and [Summaries, chapters, and highllights](/v1.3/docs/guides/analyze-videos/generate-summaries-chapters-and-highlights) pages.

# Examples

The examples in this section show how to request structured JSON responses when analyzing video content to generate open-ended text and summaries.

<Tabs>
    <Tab title="Open-ended text">
        <CodeBlocks>
            ```Python Python maxLines=8
            import json

            from twelvelabs import TwelveLabs
            from twelvelabs.types import ResponseFormat

            text = client.analyze(
                video_id="<YOUR_VIDEO_ID>",
                prompt="<YOUR_PROMPT>",
                max_tokens=2048,
                response_format=ResponseFormat(
                    json_schema={
                        "type": "object",
                        "properties": {
                            "title": {"type": "string"},
                            "summary": {"type": "string"},
                            "keywords": {"type": "array", "items": {"type": "string"}},
                        },
                    },
                ),
            )
            print(json.dumps(text.model_dump(), indent=2))
            print (f"Finish reason: {text.finish_reason}")
            ```

            ```typescript Node.js maxLines=8


            import { TwelveLabs } from "twelvelabs-js";

            const text = await client.analyze({
              videoId: "<YOUR_VIDEO_ID>",
              prompt:
                "<YOUR_PROMPT>",
              maxTokens: 2048,
              responseFormat: {
                type: "json_schema",
                jsonSchema: {
                  type: "object",
                  properties: {
                    title: {
                      type: "string",
                    },
                    summary: {
                      type: "string",
                    },
                    keywords: {
                      type: "array",
                      items: {
                        type: "string",
                      },
                    },
                  },
                },
              },
            });
            console.log(`${JSON.stringify(text, null, 2)}`);
            console.log(`Finish reason: ${text.finishReason}`);
            ```

      </CodeBlocks>
    </Tab>
    <Tab title="Open-ended text with streaming responses">
        <CodeBlocks>
            ```Python Python maxLines=8
            from twelvelabs import TwelveLabs
            from twelvelabs.types import ResponseFormat, StreamAnalyzeResponse_StreamEnd

            text_stream = client.analyze_stream(
                video_id="<YOUR_VIDEO_ID>",
                prompt="<YOUR_PROMPT>",
                max_tokens=2048,
                response_format=ResponseFormat(
                    type="json_schema",
                    json_schema={
                        "type": "object",
                        "properties": {
                            "title": {"type": "string"},
                            "summary": {"type": "string"},
                            "keywords": {"type": "array", "items": {"type": "string"}},
                        },
                    },
                ),
            )
            for chunk in text_stream:
                if chunk.event_type == "text_generation":
                    print(chunk.text, end="", flush=True)
                elif isinstance(chunk, StreamAnalyzeResponse_StreamEnd):
                    print(f"\nFinish reason: {chunk.finish_reason}")
                    if chunk.metadata and chunk.metadata.usage:
                        print(f"Usage: {chunk.metadata.usage}")
            ```

            ```typescript Node.js maxLines=8

            import { TwelveLabs } from "twelvelabs-js";

            const textStream = await client.analyzeStream({
              videoId: "<YOUR_VIDEO_ID>",
              prompt:
                "<YOUR_PROMPT>",
              maxTokens: 2048,
              responseFormat: {
                type: "json_schema",
                jsonSchema: {
                  type: "object",
                  properties: {
                    title: {
                      type: "string",
                    },
                    summary: {
                      type: "string",
                    },
                    keywords: {
                      type: "array",
                      items: {
                        type: "string",
                      },
                    },
                  },
                },
              },
            });
            for await (const chunk of textStream) {
              if (chunk.eventType === "text_generation" && "text" in chunk) {
                process.stdout.write(chunk.text!);
              } else if (chunk.eventType === "stream_end") {
                console.log(`\nFinish reason: ${chunk.finishReason}`);
                if (chunk.metadata && chunk.metadata.usage) {
                  console.log(`Usage: ${JSON.stringify(chunk.metadata.usage)}`);
                }
              }
            }
            ```

        </CodeBlocks>
    </Tab>
    <Tab title="Summarize">
        <CodeBlocks>
            ```Python Python maxLines=8
            from twelvelabs import TwelveLabs
            from twelvelabs.types import ResponseFormat

            text = client.summarize(
                video_id="<YOUR_VIDEO_ID>",
                type="summary",
                prompt="<YOUR_PROMPT>",
                response_format=ResponseFormat(
                    type="json_schema",
                    json_schema={
                        "type": "object",
                        "properties": {
                            "title": {"type": "string"},
                            "summary": {"type": "string"},
                            "keywords": {"type": "array", "items": {"type": "string"}},
                        },
                    },
                ),
            )

            if text.summarize_type == "summary":
                print(f"Summary: {text.summary}")
            ```

            ```typescript Node.js maxLines=8
            import { TwelveLabs } from "twelvelabs-js";

            const text = await client.summarize({
              videoId: "<YOUR_VIDEO_ID>",
              type: "summary",
              prompt:
                "<YOUR_PROMPT>",
              responseFormat: {
                type: "json_schema",
                jsonSchema: {
                  type: "object",
                  properties: {
                    title: {
                      type: "string",
                    },
                    summary: {
                      type: "string",
                    },
                    keywords: {
                      type: "array",
                      items: {
                        type: "string",
                      },
                    },
                  },
                },
              },
            });
            if (text.summarizeType === "summary") {
              console.log(`Summary: ${text.summary}`);
            }
            ```

        </CodeBlocks>
    </Tab>
</Tabs>

# Understanding the schema structure

The examples above use the same JSON schema to demonstrate how structured responses work:

```JSON
{
  "type": "object",
  "properties": {
    "title": {"type": "string"},
    "summary": {"type": "string"},
    "keywords": {"type": "array", "items": {"type": "string"}}
  }
}
```

This schema defines three fields that the video analysis will populate:
- `title`: A string field for the video title.
- `summary`: A string field for the video summary.
- `keywords`: An array of strings for relevant keywords.

Note that the examples also set the `max_tokens`  parameter to 2048 to limit the length of the response and reduce the risk of truncation when generating structured JSON responses. You can adjust this value up to the platform's maximum token limit of 4096 tokens.

You can define the schema to match your specific data requirements.

# Best practices

- **Start with simple schemas**: Begin with basic object structures and add complexity only when needed.
- **Keep field names descriptive**: Use clear, consistent naming conventions for schema properties to make your code more maintainable.
- **Mark essential fields as required**: Use the `required` property to specify fields that must be present. This ensures critical data is always included in responses.
- **Handle truncated responses**: For open-ended analysis, always check the `finish_reason` field in your code. When it equals `length`, use the `max_tokens` parameter to request shorter content, and implement retry logic to avoid incomplete JSON.
- **Validate responses client-side**: Parse and validate the JSON response in your application to catch any formatting issues before processing the data.
- **Test schemas thoroughly**: Validate your schema with sample data before deploying to production. Use different video types and content lengths to ensure reliability.

# JSON schema requirements

Your schema must adhere to the [JSON Schema Draft 2020-12 specification](https://json-schema.org/draft/2020-12) and must meet the requirements below:

- **Supported data types**: `array`, `boolean`, `integer`, `null`, `number`, `object`, and `string`.
- **Schema constraints**: Use validation keywords like `pattern` for strings, `minimum` and `maximum` for integers, `required` for objects, and `minItems` for arrays (accepts only 0 or 1).
- **Schema composition**: You can only use `anyOf` for combining schemas.
- **References**: Define subschemas in `$defs` and reference them with valid` $ref` URIs pointing to internal subschemas.

For complete schema specifications, see the [`json_schema`](/v1.3/api-reference/analyze-videos/analyze#request.body.response_format.json_schema) field in the API reference section.
