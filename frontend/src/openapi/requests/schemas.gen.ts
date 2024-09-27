// This file is auto-generated by @hey-api/openapi-ts

export const $Body_process_video_file_v1_process_video_file_post = {
    properties: {
        file: {
            type: 'string',
            format: 'binary',
            title: 'File'
        },
        description: {
            type: 'string',
            title: 'Description'
        },
        title: {
            type: 'string',
            title: 'Title'
        }
    },
    type: 'object',
    required: ['file', 'description', 'title'],
    title: 'Body_process_video_file_v1_process_video_file_post'
} as const;

export const $HTTPValidationError = {
    properties: {
        detail: {
            items: {
                '$ref': '#/components/schemas/ValidationError'
            },
            type: 'array',
            title: 'Detail'
        }
    },
    type: 'object',
    title: 'HTTPValidationError'
} as const;

export const $TaskOutput = {
    properties: {
        task_id: {
            type: 'string',
            title: 'Task Id'
        }
    },
    type: 'object',
    required: ['task_id'],
    title: 'TaskOutput'
} as const;

export const $ValidationError = {
    properties: {
        loc: {
            items: {
                anyOf: [
                    {
                        type: 'string'
                    },
                    {
                        type: 'integer'
                    }
                ]
            },
            type: 'array',
            title: 'Location'
        },
        msg: {
            type: 'string',
            title: 'Message'
        },
        type: {
            type: 'string',
            title: 'Error Type'
        }
    },
    type: 'object',
    required: ['loc', 'msg', 'type'],
    title: 'ValidationError'
} as const;

export const $VideoInfo = {
    properties: {
        id: {
            type: 'integer',
            title: 'Id'
        },
        file_path: {
            type: 'string',
            title: 'File Path'
        },
        status: {
            type: 'string',
            title: 'Status'
        },
        progress: {
            type: 'number',
            title: 'Progress'
        },
        result: {
            type: 'string',
            title: 'Result'
        },
        created_at: {
            type: 'string',
            format: 'date-time',
            title: 'Created At'
        },
        updated_at: {
            type: 'string',
            format: 'date-time',
            title: 'Updated At'
        }
    },
    type: 'object',
    required: ['id', 'file_path', 'status', 'progress', 'result', 'created_at', 'updated_at'],
    title: 'VideoInfo'
} as const;

export const $VideoUrlInput = {
    properties: {
        video_url: {
            type: 'string',
            maxLength: 2083,
            minLength: 1,
            format: 'uri',
            title: 'Video Url'
        }
    },
    type: 'object',
    required: ['video_url'],
    title: 'VideoUrlInput'
} as const;