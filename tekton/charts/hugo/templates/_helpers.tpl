{{- define "release.name" -}}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- end }}
