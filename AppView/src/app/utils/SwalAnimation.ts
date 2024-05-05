import Swal from "sweetalert2";


export class SwalAnimation {
    // Método para abrir el cuadro de diálogo de carga
    static mostrarCargando() {
        Swal.fire({
            title: 'Cargando',
            allowOutsideClick: false,
            didOpen: () => {
                Swal.showLoading();
            }
        });
    }

    // Método para cerrar el cuadro de diálogo de carga
    static cerrarCargando() {
        Swal.close();
    }
    static passwordSwal(): Promise<string> {
        return Swal.fire({
            title: 'Escribe tu contraseña',
            input: 'password',
            inputLabel: 'Contraseña',
            inputPlaceholder: 'Escribe tu contraseña',
            inputAttributes: {
                maxlength: '10',
                autocapitalize: 'off',
                autocorrect: 'off'
            }
        }).then((result) => {
            // Aquí puedes realizar acciones basadas en la respuesta del usuario
            if (result.isConfirmed) {
                return result.value;
            }
        });
    }

    static showConfirmCreateMessageSwal(): Promise<boolean> {
        return Swal.fire({
            title: '¿Estas seguro?',
            text: '¡Se creará!',
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            confirmButtonText: 'Si, crear!',
        }).then((result) => {
            /* Read more about isConfirmed, isDenied below */
            if (result.isConfirmed) {
                return true;
            } else if (result.isDenied) {
                return false;
            }
            return false;
        });
    }


    static showConfirmCustomMessageSwal(text: string, buttonText: string = 'Si, crear!'): Promise<boolean> {
        return Swal.fire({
            title: '¿Estas seguro?',
            text: text,
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            confirmButtonText: buttonText,
        }).then((result) => {
            /* Read more about isConfirmed, isDenied below */
            if (result.isConfirmed) {
                return true;
            } else if (result.isDenied) {
                return false;
            }
            return false;
        });
    }

    static showConfirmEditMessageSwal(): Promise<boolean> {
        return Swal.fire({
            title: '¿Estas seguro?',
            text: '¡Se actualizara!',
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            confirmButtonText: 'Si, actualizar!',
        }).then((result) => {
            /* Read more about isConfirmed, isDenied below */
            if (result.isConfirmed) {
                return true;
            } else if (result.isDenied) {
                return false;
            }
            return false;
        });
    }

    static registerPasswordSwal(): Promise<any> {
        return Swal.fire({
            title: 'Enter your passwords',
            html: `
              <label for="password">Password:</label>
              <input type="password" id="password" class="swal2-input" placeholder="Enter your password" maxlength="10" autocapitalize="off" autocorrect="off">
          
              <label for="confirmPassword">Confirm Password:</label>
              <input type="password" id="confirmPassword" class="swal2-input" placeholder="Confirm your password" maxlength="10" autocapitalize="off" autocorrect="off">
            `,
            focusConfirm: false,
            preConfirm: () => {
                const password = (<HTMLInputElement>document.getElementById('password')).value;
                const confirmPassword = (<HTMLInputElement>document.getElementById('confirmPassword')).value;
                return { password, confirmPassword };
            },
            showCancelButton: true,
            confirmButtonText: 'Next &rarr;'
        }).then((result) => {
            return result.value;
        });

    }

    static showLoading(title: string = 'Cargando...', html: string = 'Se cerrará cuando termine la consulta.') {
        Swal.fire({
            title: title,
            html: html,
            allowEscapeKey: false,
            allowOutsideClick: false,
            timerProgressBar: true,
            didOpen: () => {
                Swal.showLoading()
            }
        })
    }

    static closeLoading() {
        Swal.close();
    }



    static showLoginError() {
        Swal.fire({
            icon: 'error',
            title: 'Error en el login',
            text: 'El usuario o contraseña no son corectos',
        })
    }
    static showErrorValidationFieldTextSwal(text: string) {
        Swal.fire({
            icon: 'error',
            title: 'Error de datos',
            text: text + ' no esta correctamente o esta vacio',
        })
    }

    static showCustomSuccessSwal(title: string): void {
        Swal.fire({
            position: 'center',
            icon: 'success',
            title: title,
            showConfirmButton: false,
            timer: 1500,
        });
    }

    static showCustomErrorSwal(title: string, text: string): void {
        Swal.fire({
            icon: 'error',
            title: title,
            text: text,
        })
    }

    static showInsertedSwal(): void {
        Swal.fire({
            position: 'center',
            icon: 'success',
            title: 'Ha sido creado correctamente!',
            showConfirmButton: false,
            timer: 1500,
        });
    }

    static showInsertedNombreSwal(nombre: string): void {
        Swal.fire({
            position: 'center',
            icon: 'success',
            title: nombre + ' ha sido eliminado correctamente!',
            showConfirmButton: false,
            timer: 1500,
        });
    }

    static showErrorValidationFieldsSwal(): void {
        Swal.fire({
            icon: 'error',
            title: 'Error de datos',
            text: 'Los campos no estan correctamente o estan vacios',
        })
    }

    static showErrorValidationFieldsTextSwal(text: string): void {
        Swal.fire({
            icon: 'error',
            title: 'Error de datos',
            text: text + ' no estan correctamente o esta vacios',
        })
    }

    static showCustomWarningMessageSwal(title: string, text: string, buttonAceptarText = "Vale", buttonCancelarText = "Cancelar"): Promise<boolean> {
        return Swal.fire({
            title: title,
            text: text,
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            confirmButtonText: buttonAceptarText,
            cancelButtonText: buttonCancelarText
        }).then((result: any) => {
            /* Read more about isConfirmed, isDenied below */
            if (result.isConfirmed) {
                return true;
            } else if (result.isDenied) {
                return false;
            }
            return false;
        });
    }

    static showConfirmDeleteMessageSwal(): Promise<boolean> {
        return Swal.fire({
            title: 'Estas seguro?',
            text: '¡No podrás revertir esta acción!',
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            confirmButtonText: 'Sí, eliminar!',
        }).then((result: any) => {
            /* Read more about isConfirmed, isDenied below */
            if (result.isConfirmed) {
                return true;
            } else if (result.isDenied) {
                return false;
            }
            return false;
        });
    }
    static showConfirmVincularMessageSwal(): Promise<boolean> {
        return Swal.fire({
            title: 'Estas seguro?',
            text: '¿Seguro quieres hacer esta vinculación?',
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            confirmButtonText: 'Si, vincular!',
        }).then((result: any) => {
            /* Read more about isConfirmed, isDenied below */
            if (result.isConfirmed) {
                return true;
            } else if (result.isDenied) {
                return false;
            }
            return false;
        });
    }
    static showConfirmDesvincularMessageSwal(): Promise<boolean> {
        return Swal.fire({
            title: 'Estas seguro?',
            text: '¿Seguro quieres quitar la vinculación?',
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            confirmButtonText: 'Aceptar',
        }).then((result: any) => {
            /* Read more about isConfirmed, isDenied below */
            if (result.isConfirmed) {
                return true;
            } else if (result.isDenied) {
                return false;
            }
            return false;
        });
    }

    static show3Buttons(title: string, button1: string, button2: string, button3: string): Promise<number> {
        return Swal.fire({
            title: title,
            showDenyButton: true,
            showCancelButton: true,
            confirmButtonText: button1,
            denyButtonText: button2,
            cancelButtonText: button3
        }).then((result: any) => {
            /* Read more about isConfirmed, isDenied below */
            if (result.isConfirmed) {
                return 1;
            } else if (result.isDenied) {
                return 2;
            }
            return 0;
        });
    }

    static showSessionExpiredSwal(): void {
        Swal.fire({
            title: 'Error',
            text: 'Tu sesión a caducado',
            icon: 'error',
            confirmButtonText: 'Aceptar',
        });
    }

    static showUnauthorizedSessionSwal(): void {
        Swal.fire({
            title: 'Error',
            text: 'No estas autorizado para hacer esta acción',
            icon: 'error',
            confirmButtonText: 'Aceptar',
        });
    }

    static showModifiedSwal(nombre: string): void {
        Swal.fire({
            position: 'center',
            icon: 'success',
            title: nombre + ' ha sido modificado correctamente!',
            showConfirmButton: false,
            timer: 1500,
        });
    }

    static showDeletedSwal(): void {
        Swal.fire({
            position: 'center',
            icon: 'success',
            title: 'Ha sido eliminado correctamente!',
            showConfirmButton: false,
            timer: 1500,
        });
    }
}