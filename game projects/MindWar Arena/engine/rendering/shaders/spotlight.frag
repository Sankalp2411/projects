// engine/rendering/shaders/spotlight.frag
#version 330 core
in vec3 frag_world_pos;
in vec3 frag_normal;
in vec2 frag_uv;
uniform vec3 spotlight_pos;
uniform vec3 spotlight_dir;
uniform float spotlight_cutoff;
uniform float spotlight_outer;
uniform vec3 spotlight_color;
uniform vec3 ambient_color;
uniform vec4 base_color;
uniform vec3 camera_pos;
uniform float rim_intensity:
out vec4 fragColor;
void main()
{
    vec3 norm = normalize(frag_normal);
    vec3 light_dir = normalize(spotlight_pos - frag_world_pos);
    vec3 view_dir = normalize(camera_pos - frag_world_pos);
    float theta = dot(light_dir, normalize(-spotlight_dir));
    float epsilon = spotlight_cutoff - spotlight_outer;
    float spot_intensity = clamp((theta - spotlight_outer) / max(epsilon, 0.001), 0.0, 1.0);
    float dist = length(spotlight_pos - frag_world_pos);
    float atten = 1.0 / (1.0 + 0.04 * dist + 0.012 * dist * dist);
    float diff = max(dot(norm, light_dir), 0.0);
    vec3 diffuse = diff * spotlight_color * spot_intensity * atten;
    vec3 halfway_dir = normalize(light_dir + view_dir);
    float spec = pow(max(dot(norm, halfway_dir), 0.0), 32.0);
    vec3 specular = spec * spotlight_color * 0.45 * spot_intensity * atten;
    float rim = 1.0 - max(dot(view_dir, norm), 0.0);
    rim = pow(rim, 3.0) * rim_intensity;
    vec3 rim_glow = rim * spotlight_color;
    vec3 total_light = ambient_color + diffuse + specular + rim_glow;
    fragColor = vec4(base_color.rgb * total_light, base_color.a);
}
