// This file is auto-generated by @hey-api/openapi-ts

import type { CancelablePromise } from './core/CancelablePromise';
import { OpenAPI } from './core/OpenAPI';
import { request as __request } from './core/request';
import type { ProcessVideoUrlV1ProcessVideoUrlPostData, ProcessVideoUrlV1ProcessVideoUrlPostResponse, ProcessVideoFileV1ProcessVideoFilePostData, ProcessVideoFileV1ProcessVideoFilePostResponse, GetVideoByIdV1VideosIdGetData, GetVideoByIdV1VideosIdGetResponse, GetVideosV1VideosGetData, GetVideosV1VideosGetResponse, HealthHealthGetResponse } from './types.gen';

export class InferenceEndpointsService {
    /**
     * Process Video Url
     * Обрабатывает видео по URL
     * @param data The data for the request.
     * @param data.requestBody
     * @returns TaskOutput Successful Response
     * @throws ApiError
     */
    public static processVideoUrlV1ProcessVideoUrlPost(data: ProcessVideoUrlV1ProcessVideoUrlPostData): CancelablePromise<ProcessVideoUrlV1ProcessVideoUrlPostResponse> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/v1/process_video_url',
            body: data.requestBody,
            mediaType: 'application/json',
            errors: {
                422: 'Validation Error'
            }
        });
    }
    
    /**
     * Process Video File
     * Обрабатывает загруженное видео
     * @param data The data for the request.
     * @param data.formData
     * @returns TaskOutput Successful Response
     * @throws ApiError
     */
    public static processVideoFileV1ProcessVideoFilePost(data: ProcessVideoFileV1ProcessVideoFilePostData): CancelablePromise<ProcessVideoFileV1ProcessVideoFilePostResponse> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/v1/process_video_file',
            formData: data.formData,
            mediaType: 'multipart/form-data',
            errors: {
                422: 'Validation Error'
            }
        });
    }
    
    /**
     * Get Video By Id
     * Получает видео по идентфиикатору
     * @param data The data for the request.
     * @param data.id
     * @returns VideoRepr Successful Response
     * @throws ApiError
     */
    public static getVideoByIdV1VideosIdGet(data: GetVideoByIdV1VideosIdGetData): CancelablePromise<GetVideoByIdV1VideosIdGetResponse> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/v1/videos/{id}',
            path: {
                id: data.id
            },
            errors: {
                422: 'Validation Error'
            }
        });
    }
    
    /**
     * Get Videos
     * Получает список видео
     * @param data The data for the request.
     * @param data.skip
     * @param data.size
     * @returns VideoRepr Successful Response
     * @throws ApiError
     */
    public static getVideosV1VideosGet(data: GetVideosV1VideosGetData = {}): CancelablePromise<GetVideosV1VideosGetResponse> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/v1/videos',
            query: {
                skip: data.skip,
                size: data.size
            },
            errors: {
                422: 'Validation Error'
            }
        });
    }
    
}

export class SystemProbsService {
    /**
     * Health
     * @returns number Successful Response
     * @throws ApiError
     */
    public static healthHealthGet(): CancelablePromise<HealthHealthGetResponse> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/health'
        });
    }
    
}