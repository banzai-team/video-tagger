// generated with @7nohe/openapi-react-query-codegen@1.6.1 

import { UseQueryResult } from "@tanstack/react-query";
import { InferenceEndpointsService, SystemProbsService, VideoManagementService } from "../requests/services.gen";
export type VideoManagementServiceListVideosV1ListVideosGetDefaultResponse = Awaited<ReturnType<typeof VideoManagementService.listVideosV1ListVideosGet>>;
export type VideoManagementServiceListVideosV1ListVideosGetQueryResult<TData = VideoManagementServiceListVideosV1ListVideosGetDefaultResponse, TError = unknown> = UseQueryResult<TData, TError>;
export const useVideoManagementServiceListVideosV1ListVideosGetKey = "VideoManagementServiceListVideosV1ListVideosGet";
export const UseVideoManagementServiceListVideosV1ListVideosGetKeyFn = (queryKey?: Array<unknown>) => [useVideoManagementServiceListVideosV1ListVideosGetKey, ...(queryKey ?? [])];
export type SystemProbsServiceHealthHealthGetDefaultResponse = Awaited<ReturnType<typeof SystemProbsService.healthHealthGet>>;
export type SystemProbsServiceHealthHealthGetQueryResult<TData = SystemProbsServiceHealthHealthGetDefaultResponse, TError = unknown> = UseQueryResult<TData, TError>;
export const useSystemProbsServiceHealthHealthGetKey = "SystemProbsServiceHealthHealthGet";
export const UseSystemProbsServiceHealthHealthGetKeyFn = (queryKey?: Array<unknown>) => [useSystemProbsServiceHealthHealthGetKey, ...(queryKey ?? [])];
export type InferenceEndpointsServiceProcessVideoUrlV1ProcessVideoUrlPostMutationResult = Awaited<ReturnType<typeof InferenceEndpointsService.processVideoUrlV1ProcessVideoUrlPost>>;
export type InferenceEndpointsServiceProcessVideoFileV1ProcessVideoFilePostMutationResult = Awaited<ReturnType<typeof InferenceEndpointsService.processVideoFileV1ProcessVideoFilePost>>;
