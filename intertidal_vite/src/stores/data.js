import { defineStore } from 'pinia'
import { _generateApiResourceStore, _getPaginatedApiResources, _getApiResource } from '../_utils.js'

export const usePeopleStore = defineStore('data-people', _generateApiResourceStore((id) => `/api/people/${id}`, '/api/people'))
export const useOrganizationsStore = defineStore('data-organizations', _generateApiResourceStore((id) => `/api/organizations/${id}`, '/api/organizations'))
export const useResourcesStore = defineStore('data-resources', _generateApiResourceStore((id) => `/api/resources/${id}`, '/api/resources'))
