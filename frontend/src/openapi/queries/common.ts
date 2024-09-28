// generated with @7nohe/openapi-react-query-codegen@1.6.1 

import { UseQueryResult } from "@tanstack/react-query";
import { InferenceEndpointsService, SystemProbsService } from "../requests/services.gen";
export type InferenceEndpointsServiceGetVideoByIdV1VideosIdGetDefaultResponse = Awaited<ReturnType<typeof InferenceEndpointsService.getVideoByIdV1VideosIdGet>>;
export type InferenceEndpointsServiceGetVideoByIdV1VideosIdGetQueryResult<TData = InferenceEndpointsServiceGetVideoByIdV1VideosIdGetDefaultResponse, TError = unknown> = UseQueryResult<TData, TError>;
export const useInferenceEndpointsServiceGetVideoByIdV1VideosIdGetKey = "InferenceEndpointsServiceGetVideoByIdV1VideosIdGet";
export const UseInferenceEndpointsServiceGetVideoByIdV1VideosIdGetKeyFn = ({ id }: {
  id: unknown;
}, queryKey?: Array<unknown>) => [useInferenceEndpointsServiceGetVideoByIdV1VideosIdGetKey, ...(queryKey ?? [{ id }])];
export type InferenceEndpointsServiceGetVideosV1VideosGetDefaultResponse = Awaited<ReturnType<typeof InferenceEndpointsService.getVideosV1VideosGet>>;
export type InferenceEndpointsServiceGetVideosV1VideosGetQueryResult<TData = InferenceEndpointsServiceGetVideosV1VideosGetDefaultResponse, TError = unknown> = UseQueryResult<TData, TError>;
export const useInferenceEndpointsServiceGetVideosV1VideosGetKey = "InferenceEndpointsServiceGetVideosV1VideosGet";
export const UseInferenceEndpointsServiceGetVideosV1VideosGetKeyFn = ({ size, skip }: {
  size?: unknown;
  skip?: unknown;
} = {}, queryKey?: Array<unknown>) => [useInferenceEndpointsServiceGetVideosV1VideosGetKey, ...(queryKey ?? [{ size, skip }])];
export type SystemProbsServiceHealthHealthGetDefaultResponse = Awaited<ReturnType<typeof SystemProbsService.healthHealthGet>>;
export type SystemProbsServiceHealthHealthGetQueryResult<TData = SystemProbsServiceHealthHealthGetDefaultResponse, TError = unknown> = UseQueryResult<TData, TError>;
export const useSystemProbsServiceHealthHealthGetKey = "SystemProbsServiceHealthHealthGet";
export const UseSystemProbsServiceHealthHealthGetKeyFn = (queryKey?: Array<unknown>) => [useSystemProbsServiceHealthHealthGetKey, ...(queryKey ?? [])];
export type InferenceEndpointsServiceProcessVideoUrlV1ProcessVideoUrlPostMutationResult = Awaited<ReturnType<typeof InferenceEndpointsService.processVideoUrlV1ProcessVideoUrlPost>>;
export type InferenceEndpointsServiceProcessVideoFileV1ProcessVideoFilePostMutationResult = Awaited<ReturnType<typeof InferenceEndpointsService.processVideoFileV1ProcessVideoFilePost>>;
