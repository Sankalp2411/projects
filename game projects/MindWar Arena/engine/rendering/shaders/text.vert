#version 330 core

in vec2 in_position;
in vec2 in_uv;

out vec2 uv;

uniform mat4 projection;

void main()
{
    uv = in_uv;

    gl_Position = projection * vec4(
        in_position,
        0.0,
        1.0
    );
}